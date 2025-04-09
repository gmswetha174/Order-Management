from entities.product import Product

class Electronics(Product):
    def __init__(self, product_id=0, product_name="", description="", price=0.0, quantity_in_stock=0, brand="", warranty_period=0):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, "Electronics")
        self.brand = brand
        self.warranty_period = warranty_period

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def warranty_period(self):
        return self._warranty_period

    @warranty_period.setter
    def warranty_period(self, value):
        self._warranty_period = value

    def __str__(self):
        return super().__str__() + f", Brand: {self.brand}, Warranty: {self.warranty_period} months"