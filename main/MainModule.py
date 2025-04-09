# main/main_module.py

from entity.customer import User
from entity.product import Electronics, Clothing
from dao.customer_dao import CustomerDAO
from dao.product_dao import ProductDAO
from dao.order_dao import OrderDAO
from exceptions.exceptions import UserNotFoundException
from exceptions.exceptions import OrderNotFoundException

def main():
    customer_dao = CustomerDAO()
    product_dao = ProductDAO()
    order_dao = OrderDAO()

    while True:
        print("\n📦 Order Management System Menu:")
        print("1. Create User")
        print("2. Create Product")
        print("3. Place Order")
        print("4. Cancel Order")
        print("5. Get All Products")
        print("6. Get Orders by User")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            role = input("Enter Role (Admin/User): ")
            user = User(None, username, password, role)
            customer_dao.create_user(user)

        elif choice == "2":
            userId = int(input("Enter Admin User ID: "))
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            role = "Admin"
            admin = User(userId, username, password, role)

            print("Product Type (Electronics/Clothing): ", end="")
            ptype = input().strip()

            name = input("Enter Product Name: ")
            desc = input("Enter Description: ")
            price = float(input("Enter Price: "))
            quantity = int(input("Enter Quantity In Stock: "))

            if ptype.lower() == "electronics":
                brand = input("Enter Brand: ")
                warranty = int(input("Enter Warranty Period (months): "))
                product = Electronics(0, name, desc, price, quantity, brand, warranty)
            else:
                size = input("Enter Size: ")
                color = input("Enter Color: ")
                product = Clothing(0, name, desc, price, quantity, size, color)

            try:
                product_dao.create_product(product)
            except UserNotFoundException as e:
                print(e)

        elif choice == "3":
            userId = int(input("Enter User ID: "))
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            role = "User"
            user = User(userId, username, password, role)

            product_ids = list(map(int, input("Enter product IDs to order (comma separated): ").split(',')))
            try:
                order_dao.create_order(user, product_ids)
            except Exception as e:
                print(e)

        elif choice == "4":
            userId = int(input("Enter User ID: "))
            order_id = int(input("Enter Order ID: "))
            try:
                order_dao.cancel_order(userId, order_id)
            except (UserNotFoundException, OrderNotFoundException) as e:
                print(e)

        elif choice == "5":
            products = product_dao.get_all_products()
            for p in products:
                print(p)

        elif choice == "6":
            userId = int(input("Enter User ID: "))
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            role = "User"
            user = User(userId, username, password, role)
            orders = order_dao.get_orders_by_user(user)
            for o in orders:
                print(o)

        elif choice == "7":
            print("👋 Exiting Order Management System.")
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
