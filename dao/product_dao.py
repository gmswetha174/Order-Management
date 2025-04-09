# dao/product_dao.py

import mysql.connector
from entity.product import Product, Electronics, Clothing
from util.db_connection import DBConnUtil

class ProductDAO:
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def create_product(self, product):
        try:
            cursor = self.connection.cursor()

            # Insert into Product table first
            product_query = """
                INSERT INTO Product (productName, description, price, quantityInStock, type)
                VALUES (%s, %s, %s, %s, %s)
            """
            product_data = (
                product.product_name, product.description, product.price,
                product.quantity_in_stock, product.product_type
            )
            cursor.execute(product_query, product_data)
            product_id = cursor.lastrowid  # Get auto-generated productId

            # Insert into Electronics or Clothing table
            if isinstance(product, Electronics):
                electronics_query = """
                    INSERT INTO Electronics (productId, brand, warrantyPeriod)
                    VALUES (%s, %s, %s)
                """
                electronics_data = (product_id, product.brand, product.warranty_period)
                cursor.execute(electronics_query, electronics_data)

            elif isinstance(product, Clothing):
                clothing_query = """
                    INSERT INTO Clothing (productId, size, color)
                    VALUES (%s, %s, %s)
                """
                clothing_data = (product_id, product.size, product.color)
                cursor.execute(clothing_query, clothing_data)

            else:
                raise ValueError("Invalid product type")

            self.connection.commit()
            print("✅ Product created successfully!")

        except mysql.connector.Error as e:
            print(f"❌ Error inserting product: {e}")



    def get_all_products(self):
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Get Electronics
            cursor.execute("SELECT * FROM electronics")
            electronics = cursor.fetchall()

            # Get Clothing
            cursor.execute("SELECT * FROM clothing")
            clothing = cursor.fetchall()

            return electronics + clothing

        except mysql.connector.Error as e:
            print(f"❌ Error fetching products: {e}")
            return []
