import hashlib
import os

# A simple dictionary to store user data for demonstration purposes
# In a real app, use a secure database
user_db = {}

def hash_password(password):
    """
    Hash a password for storing it securely.
    
    Parameters:
    - password (str): The user's password in plain text.
    
    Returns:
    - str: A hashed password.
    """
    salt = os.urandom(16)  # Generate a random 16-byte salt
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + hashed_password  # Return the salt and the hash combined

def verify_password(stored_password, provided_password):
    """
    Verify a stored password against one provided by the user.
    
    Parameters:
    - stored_password (bytes): The stored salt+hash password.
    - provided_password (str): The password provided for verification.
    
    Returns:
    - bool: True if the password is correct, False otherwise.
    """
    salt = stored_password[:16]  # Extract the salt from the stored password
    stored_hash = stored_password[16:]  # Extract the hash
    provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return provided_hash == stored_hash

def register_user(username, password):
    """
    Register a new user by hashing and storing their password.
    
    Parameters:
    - username (str): The user's chosen username.
    - password (str): The user's chosen password.
    
    Returns:
    - str: A message indicating the result of the registration attempt.
    """
    if username in user_db:
        return "Error: Username already exists."

    user_db[username] = hash_password(password)
    return "Registration successful!"

def login_user(username, password):
    """
    Log in a user by verifying their password.
    
    Parameters:
    - username (str): The user's username.
    - password (str): The user's password.
    
    Returns:
    - str: A message indicating the result of the login attempt.
    """
    if username not in user_db:
        return "Error: Username not found."

    if verify_password(user_db[username], password):
        return "Login successful!"
    else:
        return "Error: Incorrect password."


