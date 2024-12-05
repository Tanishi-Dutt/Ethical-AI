from cryptography.fernet import Fernet
import bcrypt  # Corrected import for bcrypt

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Decrypt data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify a password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Example usage
if __name__ == "__main__":
    # Generate encryption key
    key = generate_key()
    print("Encryption Key:", key)
    # Example data for encryption
    data = "Sensitive data"
    encrypted = encrypt_data(data, key)
    print("Encrypted:", encrypted)
    
    decrypted = decrypt_data(encrypted, key)
    print("Decrypted:", decrypted)
    
    # Example password hashing
    password = "my_secret_password"
    hashed_password = hash_password(password)
    print("Hashed Password:", hashed_password)
    
    # Verify password
    is_correct = verify_password(hashed_password, password)
    print("Password Match:", is_correct)
