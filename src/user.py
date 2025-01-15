

from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self,username,password):
        """
        Initialize a user object with username,password, and role
        """

        self.username=username
        self.original_password=password
        self.password=generate_password_hash(password)

    def verify_password(self,password):

        return check_password_hash(self.password,password)

    def __str__(self):

        return f"Username: {self.username}"
