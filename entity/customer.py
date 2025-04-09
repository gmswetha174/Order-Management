# entity/customer.py

class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role  # "Admin" or "User"

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role

    def __str__(self):
        return f"User[ID={self.user_id}, Username={self.username}, Role={self.role}]"
