# dao/order_dao.py

import mysql.connector
from entity.customer import User
from entity.product import Product
from entity.order import Order
from util.db_connection import DBConnUtil
from exceptions.exceptions import UserNotFoundException, OrderNotFoundException

class OrderDAO:
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def create_order(self, user: User, product_ids: list):
        try:
            cursor = self.connection.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM User WHERE userId = %s", (user.user_id,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {user.user_id} not found.")

            # Insert new order
            cursor.execute("INSERT INTO Orders (userId) VALUES (%s)", (user.user_id,))
            order_id = cursor.lastrowid

            # Insert into Order_Product
            for pid in product_ids:
                cursor.execute("INSERT INTO Order_Product (orderId, productId, quantity) VALUES (%s, %s, %s)", (order_id, pid, 1))

            self.connection.commit()
            print(f"✅ Order {order_id} created successfully!")

        except mysql.connector.Error as e:
            print(f"❌ Error creating order: {e}")

    def cancel_order(self, user_id: int, order_id: int):
        try:
            cursor = self.connection.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM User WHERE userId = %s", (user_id,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {user_id} not found.")

            # Check if order exists
            cursor.execute("SELECT * FROM Orders WHERE orderId = %s AND userId = %s", (order_id, user_id))
            if not cursor.fetchone():
                raise OrderNotFoundException(f"Order {order_id} not found for User {user_id}.")

            # Delete order and associated products
            cursor.execute("DELETE FROM Order_Product WHERE orderId = %s", (order_id,))
            cursor.execute("DELETE FROM Orders WHERE orderId = %s", (order_id,))
            self.connection.commit()

            print(f"🗑️ Order {order_id} cancelled successfully!")

        except mysql.connector.Error as e:
            print(f"❌ Error cancelling order: {e}")

    def get_orders_by_user(self, user: User):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT o.orderId, p.productId, p.productName, p.price 
                FROM Orders o 
                JOIN Order_Product op ON o.orderId = op.orderId
                JOIN Product p ON op.productId = p.productId
                WHERE o.userId = %s
            """
            cursor.execute(query, (user.user_id,))
            return cursor.fetchall()

        except mysql.connector.Error as e:
            print(f"❌ Error retrieving orders: {e}")
            return []
