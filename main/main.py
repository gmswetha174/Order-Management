from typing import List
from entities.product import Product
from entities.electronics import Electronics
from entities.clothing import Clothing
from entities.user import User
from exceptions.user_not_found import UserNotFoundException
from exceptions.order_not_found import OrderNotFoundException
from dao.order_processor import OrderProcessor

def display_menu():
    print("\n===== Order Management System =====")
    print("1. Create User")
    print("2. Create Product (Admin only)")
    print("3. Create Order")
    print("4. Cancel Order")
    print("5. Get All Products")
    print("6. Get Orders by User")
    print("7. Exit")
    return input("Enter your choice: ")

def create_user(order_processor: OrderProcessor):
    print("\n--- Create New User ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (Admin/User): ")
    
    user = User(0, username, password, role)
    order_processor.create_user(user)

def create_product(order_processor: OrderProcessor):
    print("\n--- Create New Product ---")
    
    user_id = int(input("Enter admin user ID: "))
    product_type = input("Enter product type (Electronics/Clothing): ").capitalize()
    
    name = input("Enter product name: ")
    description = input("Enter description: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity in stock: "))
    
    user = User(user_id)
    
    if product_type == "Electronics":
        brand = input("Enter brand: ")
        warranty = int(input("Enter warranty period (months): "))
        product = Electronics(0, name, description, price, quantity, brand, warranty)
    else:
        size = input("Enter size: ")
        color = input("Enter color: ")
        product = Clothing(0, name, description, price, quantity, size, color)
    
    try:
        order_processor.create_product(user, product)
    except UserNotFoundException as e:
        print(f"Error: {e}")

def create_order(order_processor: OrderProcessor):
    print("\n--- Create New Order ---")
    
    user_id = int(input("Enter user ID: "))
    products = []
    
    while True:
        product_id = input("Enter product ID to add to order (or 'done' to finish): ")
        if product_id.lower() == 'done':
            break
        
        try:
            product_id = int(product_id)
            product = Product(product_id)
            products.append(product)
        except ValueError:
            print("Please enter a valid product ID or 'done'")
    
    if products:
        user = User(user_id)
        try:
            order_processor.create_order(user, products)
        except UserNotFoundException as e:
            print(f"Error: {e}")

def cancel_order(order_processor: OrderProcessor):
    print("\n--- Cancel Order ---")
    
    user_id = int(input("Enter user ID: "))
    order_id = int(input("Enter order ID to cancel: "))
    
    try:
        order_processor.cancel_order(user_id, order_id)
    except (UserNotFoundException, OrderNotFoundException) as e:
        print(f"Error: {e}")

def get_all_products(order_processor: OrderProcessor):
    print("\n--- All Products ---")
    products = order_processor.get_all_products()
    
    if not products:
        print("No products available.")
    else:
        for product in products:
            print(product)

def get_orders_by_user(order_processor: OrderProcessor):
    print("\n--- Orders by User ---")
    
    user_id = int(input("Enter user ID: "))
    user = User(user_id)
    
    try:
        products = order_processor.get_order_by_user(user)
        
        if not products:
            print("No orders found for this user.")
        else:
            print(f"Orders for user ID {user_id}:")
            for product in products:
                print(product)
    except UserNotFoundException as e:
        print(f"Error: {e}")

def main():
    order_processor = OrderProcessor()
    
    while True:
        choice = display_menu()
        
        try:
            if choice == '1':
                create_user(order_processor)
            elif choice == '2':
                create_product(order_processor)
            elif choice == '3':
                create_order(order_processor)
            elif choice == '4':
                cancel_order(order_processor)
            elif choice == '5':
                get_all_products(order_processor)
            elif choice == '6':
                get_orders_by_user(order_processor)
            elif choice == '7':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()