from entities.product import Product

class Clothing(Product):
    def __init__(self, product_id=0, product_name="", description="", price=0.0, quantity_in_stock=0, size="", color=""):
        super().__init__(product_id, product_name, description, price, quantity_in_stock, "Clothing")
        self.size = size
        self.color = color

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __str__(self):
        return super().__str__() + f", Size: {self.size}, Color: {self.color}"