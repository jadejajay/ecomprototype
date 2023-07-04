import hashlib
import os
from colorama import init, Fore, Style
init()
class User:
    def __init__(self, username, password):
        self.username = username
        self.salt = self.generate_salt()
        self.password_hash = self.hash_password(password)

    def generate_salt(self):
        # Generate a random salt value
        return os.urandom(16)

    def hash_password(self, password):
        # Combine the password and salt
        salted_password = password.encode() + self.salt

        # Hash the salted password using a hash function (e.g., SHA-256)
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        return hashed_password

    def validate_password(self, password):
        # Hash the provided password with the stored salt
        hashed_password = self.hash_password(password)

        # Compare the hashed password with the stored hash
        return hashed_password == self.password_hash


class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def login(self, username, password):
        for user in self.users:
            if user.username == username:
                if user.validate_password(password):
                    print(Fore.GREEN,"Login successful!")
                    return
                else:
                    print(Fore.RED,"Invalid password.")
                    return
        print(Fore.LIGHTRED_EX,"User not found.")


# Create some example users
user1 = User("alice", "password1")
user2 = User("bob", "password2")
user3 = User("charlie", "password3")

# Create a user manager and add the users
user_manager = UserManager()
user_manager.add_user(user1)
user_manager.add_user(user2)
user_manager.add_user(user3)

# User login example
user_manager.login("alice", "password1")  # Valid login
user_manager.login("bob", "wrongpassword")  # Invalid password
user_manager.login("lied", "password")  # User not found
