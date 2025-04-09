class User:
    def __init__(self, user_id=0, username="", password="", role=""):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    def __str__(self):
        return f"User(ID: {self.user_id}, Username: {self.username}, Role: {self.role})"