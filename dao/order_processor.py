from typing import List
import mysql.connector
from mysql.connector import Error
from entities.product import Product
from entities.electronics import Electronics
from entities.clothing import Clothing
from entities.user import User
from exceptions.user_not_found import UserNotFoundException
from exceptions.order_not_found import OrderNotFoundException
from exceptions.product_not_found import ProductNotFoundException
from utils.db_conn_util import DBConnUtil
from dao.order_repository import IOrderManagementRepository

class OrderProcessor(IOrderManagementRepository):
    def __init__(self):
        self.connection = DBConnUtil.get_connection()
        self.cursor = self.connection.cursor(dictionary=True)
    
    def create_order(self, user: User, products: List[Product]):
        try:
            # Check if user exists
            if not self._is_user_exists(user.user_id):
                raise UserNotFoundException(f"User with ID {user.user_id} not found.")
            
            # Start transaction
            self.connection.start_transaction()
            
            try:
                # Create order
                self.cursor.execute(
                    "INSERT INTO Orders (userId) VALUES (%s)",
                    (user.user_id,)
                )
                order_id = self.cursor.lastrowid
                
                # Add order details
                for product in products:
                    # Check if product exists
                    if not self._is_product_exists(product.product_id):
                        raise ProductNotFoundException(f"Product with ID {product.product_id} not found.")
                    
                    # Check stock availability
                    if not self._is_product_available(product.product_id, 1):
                        raise ProductNotFoundException(f"Product with ID {product.product_id} is out of stock.")
                    
                    # Add to order details
                    self.cursor.execute(
                        "INSERT INTO OrderDetails (orderId, productId, quantity) VALUES (%s, %s, %s)",
                        (order_id, product.product_id, 1)
                    )
                    
                    # Update product stock
                    self._update_product_stock(product.product_id, -1)
                
                # Commit transaction
                self.connection.commit()
                print("Order created successfully!")
                
            except Exception as e:
                # Rollback on error
                self.connection.rollback()
                raise e
                
        except Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def cancel_order(self, user_id: int, order_id: int):
        try:
            # Check if user exists
            if not self._is_user_exists(user_id):
                raise UserNotFoundException(f"User with ID {user_id} not found.")
            
            # Check if order exists and belongs to user
            if not self._is_order_exists_for_user(order_id, user_id):
                raise OrderNotFoundException(f"Order with ID {order_id} not found for user {user_id}")
            
            # Start transaction
            self.connection.start_transaction()
            
            try:
                # Get order details to restore product quantities
                self.cursor.execute(
                    "SELECT productId, quantity FROM OrderDetails WHERE orderId = %s",
                    (order_id,)
                )
                products = self.cursor.fetchall()
                
                # Restore product quantities
                for product in products:
                    self._update_product_stock(product['productId'], product['quantity'])
                
                # Delete order details
                self.cursor.execute(
                    "DELETE FROM OrderDetails WHERE orderId = %s",
                    (order_id,)
                )
                
                # Delete order
                self.cursor.execute(
                    "DELETE FROM Orders WHERE orderId = %s",
                    (order_id,)
                )
                
                # Commit transaction
                self.connection.commit()
                print("Order cancelled successfully!")
                
            except Exception as e:
                # Rollback on error
                self.connection.rollback()
                raise e
                
        except Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def create_product(self, user: User, product: Product):
        try:
            # Check if user is admin
            if not self._is_user_admin(user.user_id):
                raise UserNotFoundException(f"User with ID {user.user_id} is not authorized to create products.")
            
            # Start transaction
            self.connection.start_transaction()
            
            try:
                # Insert into Products table
                self.cursor.execute(
                    "INSERT INTO Products (productName, description, price, quantityInStock, type) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (
                        product.product_name,
                        product.description,
                        product.price,
                        product.quantity_in_stock,
                        product.type
                    )
                )
                product_id = self.cursor.lastrowid
                
                # Insert into specific product type table
                if isinstance(product, Electronics):
                    self.cursor.execute(
                        "INSERT INTO Electronics (productId, brand, warrantyPeriod) "
                        "VALUES (%s, %s, %s)",
                        (
                            product_id,
                            product.brand,
                            product.warranty_period
                        )
                    )
                elif isinstance(product, Clothing):
                    self.cursor.execute(
                        "INSERT INTO Clothing (productId, size, color) "
                        "VALUES (%s, %s, %s)",
                        (
                            product_id,
                            product.size,
                            product.color
                        )
                    )
                
                # Commit transaction
                self.connection.commit()
                print("Product created successfully!")
                
            except Exception as e:
                # Rollback on error
                self.connection.rollback()
                raise e
                
        except Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def create_user(self, user: User):
        try:
            self.cursor.execute(
                "INSERT INTO Users (username, password, role) "
                "VALUES (%s, %s, %s)",
                (
                    user.username,
                    user.password,
                    user.role
                )
            )
            self.connection.commit()
            print("User created successfully!")
        except Error as e:
            print(f"Database error: {e}")
    
    def get_all_products(self) -> List[Product]:
        products = []
        try:
            self.cursor.execute(
                "SELECT p.*, e.brand, e.warrantyPeriod, c.size, c.color "
                "FROM Products p "
                "LEFT JOIN Electronics e ON p.productId = e.productId "
                "LEFT JOIN Clothing c ON p.productId = c.productId"
            )
            
            for row in self.cursor.fetchall():
                if row['type'] == 'Electronics':
                    product = Electronics(
                        row['productId'],
                        row['productName'],
                        row['description'],
                        row['price'],
                        row['quantityInStock'],
                        row['brand'],
                        row['warrantyPeriod']
                    )
                else:
                    product = Clothing(
                        row['productId'],
                        row['productName'],
                        row['description'],
                        row['price'],
                        row['quantityInStock'],
                        row['size'],
                        row['color']
                    )
                products.append(product)
                
        except Error as e:
            print(f"Database error: {e}")
        
        return products
    
    def get_order_by_user(self, user: User) -> List[Product]:
        products = []
        try:
            # Check if user exists
            if not self._is_user_exists(user.user_id):
                raise UserNotFoundException(f"User with ID {user.user_id} not found.")
            
            self.cursor.execute(
                "SELECT p.*, e.brand, e.warrantyPeriod, c.size, c.color "
                "FROM Products p "
                "LEFT JOIN Electronics e ON p.productId = e.productId "
                "LEFT JOIN Clothing c ON p.productId = c.productId "
                "JOIN OrderDetails od ON p.productId = od.productId "
                "JOIN Orders o ON od.orderId = o.orderId "
                "WHERE o.userId = %s",
                (user.user_id,)
            )
            
            for row in self.cursor.fetchall():
                if row['type'] == 'Electronics':
                    product = Electronics(
                        row['productId'],
                        row['productName'],
                        row['description'],
                        row['price'],
                        row['quantityInStock'],
                        row['brand'],
                        row['warrantyPeriod']
                    )
                else:
                    product = Clothing(
                        row['productId'],
                        row['productName'],
                        row['description'],
                        row['price'],
                        row['quantityInStock'],
                        row['size'],
                        row['color']
                    )
                products.append(product)
                
        except Error as e:
            print(f"Database error: {e}")
        
        return products
    
    # Helper methods
    def _is_user_exists(self, user_id: int) -> bool:
        self.cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE userId = %s",
            (user_id,)
        )
        return self.cursor.fetchone()['COUNT(*)'] > 0
    
    def _is_user_admin(self, user_id: int) -> bool:
        self.cursor.execute(
            "SELECT role FROM Users WHERE userId = %s",
            (user_id,)
        )
        row = self.cursor.fetchone()
        return row and row['role'] == 'Admin'
    
    def _is_product_exists(self, product_id: int) -> bool:
        self.cursor.execute(
            "SELECT COUNT(*) FROM Products WHERE productId = %s",
            (product_id,)
        )
        return self.cursor.fetchone()['COUNT(*)'] > 0
    
    def _is_product_available(self, product_id: int, quantity: int) -> bool:
        self.cursor.execute(
            "SELECT quantityInStock FROM Products WHERE productId = %s",
            (product_id,)
        )
        row = self.cursor.fetchone()
        return row and row['quantityInStock'] >= quantity
    
    def _is_order_exists_for_user(self, order_id: int, user_id: int) -> bool:
        self.cursor.execute(
            "SELECT COUNT(*) FROM Orders WHERE orderId = %s AND userId = %s",
            (order_id, user_id)
        )
        return self.cursor.fetchone()['COUNT(*)'] > 0
    
    def _update_product_stock(self, product_id: int, quantity_change: int):
        self.cursor.execute(
            "UPDATE Products SET quantityInStock = quantityInStock + %s WHERE productId = %s",
            (quantity_change, product_id)
        )
    
    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            DBConnUtil.close_connection(self.connection)