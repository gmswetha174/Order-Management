# entity/product.py

class Product:
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, product_type):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.product_type = product_type  # "Electronics" or "Clothing"

    def get_product_id(self):
        return self.product_id

    def get_product_name(self):
        return self.product_name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_quantity_in_stock(self):
        return self.quantity_in_stock

    def get_product_type(self):
        return self.product_type

    def set_quantity_in_stock(self, quantity):
        self.quantity_in_stock = quantity

    def __str__(self):
        return f"{self.product_id} - {self.product_name} ({self.product_type}) - ₹{self.price}"


class Electronics(Product):
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, brand, warranty_period):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, "Electronics")
        self.brand = brand
        self.warranty_period = warranty_period

    def get_brand(self):
        return self.brand

    def get_warranty_period(self):
        return self.warranty_period

    def __str__(self):
        return super().__str__() + f" | Brand: {self.brand}, Warranty: {self.warranty_period} months"


class Clothing(Product):
    def __init__(self, product_id, product_name, description, price, quantity_in_stock, size, color):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, "Clothing")
        self.size = size
        self.color = color

    def get_size(self):
        return self.size

    def get_color(self):
        return self.color

    def __str__(self):
        return super().__str__() + f" | Size: {self.size}, Color: {self.color}"
