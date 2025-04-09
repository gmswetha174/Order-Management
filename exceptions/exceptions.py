# exceptions/exceptions.py

class UserNotFoundException(Exception):
    def __init__(self, message="User not found in the database"):
        super().__init__(message)


class OrderNotFoundException(Exception):
    def __init__(self, message="Order not found in the database"):
        super().__init__(message)

class ProductNotFoundException(Exception):
    def __init__(self, message="Product not found in the database"):
        super().__init__(message)

class InvalidUserRoleException(Exception):
    def __init__(self, message="Invalid user role. Access denied."):
        super().__init__(message)
