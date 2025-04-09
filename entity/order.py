# entity/order.py

class Order:
    def __init__(self, order_id, user_id, product_id, quantity):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def get_order_id(self):
        return self.order_id

    def get_user_id(self):
        return self.user_id

    def get_product_id(self):
        return self.product_id

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Order[OrderID={self.order_id}, UserID={self.user_id}, ProductID={self.product_id}, Quantity={self.quantity}]"
