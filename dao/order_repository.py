from abc import ABC, abstractmethod
from typing import List
from entities.product import Product
from entities.user import User

class IOrderManagementRepository(ABC):
    @abstractmethod
    def create_order(self, user: User, products: List[Product]):
        pass
    
    @abstractmethod
    def cancel_order(self, user_id: int, order_id: int):
        pass
    
    @abstractmethod
    def create_product(self, user: User, product: Product):
        pass
    
    @abstractmethod
    def create_user(self, user: User):
        pass
    
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass
    
    @abstractmethod
    def get_order_by_user(self, user: User) -> List[Product]:
        pass