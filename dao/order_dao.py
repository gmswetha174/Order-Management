# dao/order_dao.py

import mysql.connector
from entity.customer import User
from entity.product import Product
from entity.order import Order
from util.db_connection import DBConnUtil
from exceptions.exceptions import UserNotFoundException
from exceptions.exceptions import OrderNotFoundException

class OrderDAO:
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def create_order(self, user: User, product_ids: list):
        try:
            cursor = self.connection.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM user WHERE userId = %s", (user.userId,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {user.userId} not found.")

            # Insert new order
            cursor.execute("INSERT INTO `order` (userId) VALUES (%s)", (user.userId,))
            order_id = cursor.lastrowid

            # Insert into order_product
            for pid in product_ids:
                cursor.execute("INSERT INTO order_product (order_id, product_id) VALUES (%s, %s)", (order_id, pid))

            self.connection.commit()
            print(f"✅ Order {order_id} created successfully!")

        except mysql.connector.Error as e:
            print(f"❌ Error creating order: {e}")

    def cancel_order(self, userId: int, order_id: int):
        try:
            cursor = self.connection.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM user WHERE userId = %s", (userId,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {userId} not found.")

            # Check if order exists
            cursor.execute("SELECT * FROM `order` WHERE order_id = %s AND userId = %s", (order_id, userId))
            if not cursor.fetchone():
                raise OrderNotFoundException(f"Order {order_id} not found for User {userId}.")

            # Delete order and associated products
            cursor.execute("DELETE FROM order_product WHERE order_id = %s", (order_id,))
            cursor.execute("DELETE FROM `order` WHERE order_id = %s", (order_id,))
            self.connection.commit()

            print(f"🗑️ Order {order_id} cancelled successfully!")

        except mysql.connector.Error as e:
            print(f"❌ Error cancelling order: {e}")

    def get_orders_by_user(self, user: User):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT o.order_id, p.product_id, p.product_name, p.price 
                FROM `order` o 
                JOIN order_product op ON o.order_id = op.order_id
                JOIN product p ON op.product_id = p.product_id
                WHERE o.userId = %s
            """
            cursor.execute(query, (user.userId,))
            return cursor.fetchall()

        except mysql.connector.Error as e:
            print(f"❌ Error retrieving orders: {e}")
            return []
