# dao/customer_dao.py

import mysql.connector
from entity.customer import User
from util.db_connection import DBConnUtil
from exceptions.exceptions import UserNotFoundException

class CustomerDAO:
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def create_user(self, user: User):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)"
            data = (user.username, user.password, user.role)
            cursor.execute(query, data)
            self.connection.commit()
            userId = cursor.lastrowid  # Get auto-generated user ID
            print(f"✅ User created successfully with ID: {userId}")

        except mysql.connector.Error as e:
            print(f"❌ Error creating user: {e}")

    def get_user_by_id(self, userId: int):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM user WHERE userId = %s"
            cursor.execute(query, (userId,))
            result = cursor.fetchone()

            if not result:
                raise UserNotFoundException(f"User with ID {userId} not found.")

            return User(
                userId=result['userId'],
                username=result['username'],
                password=result['password'],
                role=result['role']
            )

        except mysql.connector.Error as e:
            print(f"❌ Error fetching user: {e}")
            return None
