#shiven
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import bcrypt

# --- Rayyana's Encryption Functions (Modified for Integration) ---
# Generate a Fernet encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt data with Fernet symmetric encryption
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Decrypt data with Fernet symmetric encryption
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Hash a password (for secure login if needed)
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify a password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# --- RSA Key Generation for Asymmetric Encryption ---
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Serialize public key for sharing
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

# Load public key from serialized format
def load_public_key(serialized_public_key):
    return serialization.load_pem_public_key(serialized_public_key)

# Encrypt Fernet key with recipient's public RSA key
def encrypt_fernet_key_with_public_key(fernet_key, public_key):
    encrypted_key = public_key.encrypt(
        fernet_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

# Decrypt Fernet key with recipient's private RSA key
def decrypt_fernet_key_with_private_key(encrypted_fernet_key, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_fernet_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key

# --- Combined Secure Messaging System ---
# Encrypt a message for secure transmission
def encrypt_message_for_user(message, recipient_public_key):
    # Step 1: Generate a Fernet key and encrypt the message with it
    fernet_key = generate_key()
    encrypted_message = encrypt_data(message, fernet_key)

    # Step 2: Encrypt the Fernet key with recipient's public RSA key
    encrypted_fernet_key = encrypt_fernet_key_with_public_key(fernet_key, recipient_public_key)

    # Return both the encrypted message and the encrypted Fernet key
    return encrypted_message, encrypted_fernet_key

# Decrypt the received message
def decrypt_received_message(encrypted_message, encrypted_fernet_key, recipient_private_key):
    # Step 1: Decrypt the Fernet key with recipient's private RSA key
    fernet_key = decrypt_fernet_key_with_private_key(encrypted_fernet_key, recipient_private_key)

    # Step 2: Use the decrypted Fernet key to decrypt the message
    decrypted_message = decrypt_data(encrypted_message, fernet_key)

    return decrypted_message

# Example usage for secure messaging
if __name__ == "__main__":
    # Generate RSA key pairs for two users (e.g., User1 and User2)
    user1_private_key, user1_public_key = generate_rsa_key_pair()
    user2_private_key, user2_public_key = generate_rsa_key_pair()

    # Serialize user2's public key (for user1 to encrypt a message to user2)
    user2_serialized_public_key = serialize_public_key(user2_public_key)
    user2_loaded_public_key = load_public_key(user2_serialized_public_key)

    # User1 encrypts a message for User2
    message = "Hello, User2! This is a secure message."
    encrypted_message, encrypted_fernet_key = encrypt_message_for_user(message, user2_loaded_public_key)
    print("Encrypted Message:", encrypted_message)
    print("Encrypted Fernet Key:", encrypted_fernet_key)

    # User2 decrypts the message with their private key
    decrypted_message = decrypt_received_message(encrypted_message, encrypted_fernet_key, user2_private_key)
    print("Decrypted Message:", decrypted_message)

