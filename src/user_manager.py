import csv
from user import User

class UserManager:
    def __init__(self):
        self.users = []  # List of user objects
        self.load_users()

    def load_users(self):
        """
        Load users from the users.csv file.
        """
        try:
            with open("../csv_files/users.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the title line
                for row in reader:
                    username, password = row
                    user = User(username, password)
                    user.original_password = password  # Load the plain text password
                    self.users.append(user)
            print("Users loaded successfully:", [user.username for user in self.users])

        except FileNotFoundError:
            print("users.csv not found...starting with an empty user list")
        except Exception as e:
            print(f"Error loading users: {e}")

    def save_users(self):
        """
        Save users to the users.csv file.
        """
        try:
            with open("../csv_files/users.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])  # Write the header
                for user in self.users:
                    writer.writerow([user.username, user.original_password])  # Save plain text password
            print("Users saved successfully!")
        except Exception as e:
            print(f"Error saving users: {e}")

    def add_user(self, username, password):
        """
        Add a new user to the system.
        """
        if any(user.username == username for user in self.users):
            print(f"Username {username} already exists")
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()  # Save the user with the plain text password
        print(f"User {username} added successfully")
        return True

    def authenticate_user(self, username, password):
        """
        Authenticate a user by username and password.
        """
        for user in self.users:
            if user.username == username and user.verify_password(password):  # Verify hashed password
                print(f"User {username} authenticated successfully!")
                return user
        print("Authentication failed.")
        return None