from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import bcrypt

def generate_key():
    """Generate a Fernet encryption key."""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """Encrypt data using Fernet symmetric encryption."""
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    """Decrypt data using Fernet symmetric encryption."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

def hash_password(password):
    """Hash a password for secure storage."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    """Verify a provided password against the stored hashed password."""
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# --- RSA Key Generation for Asymmetric Encryption ---
def generate_rsa_key_pair():
    """Generate a private-public RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    """Serialize the public key for sharing."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def load_public_key(serialized_public_key):
    """Load a public key from the serialized format."""
    return serialization.load_pem_public_key(serialized_public_key)

def encrypt_fernet_key_with_public_key(fernet_key, public_key):
    """Encrypt a Fernet key using the recipient's public RSA key."""
    encrypted_key = public_key.encrypt(
        fernet_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

def decrypt_fernet_key_with_private_key(encrypted_fernet_key, private_key):
    """Decrypt a Fernet key using the recipient's private RSA key."""
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
def encrypt_message_for_user(message, recipient_public_key):
    """
    Encrypt a message for secure transmission to a recipient's public key.
    
    Parameters:
    - message (str): The message to be sent securely.
    - recipient_public_key: The recipient's public key for encryption.
    
    Returns:
    Tuple of encrypted message and encrypted Fernet key.
    """
    fernet_key = generate_key()  # Step 1: Generate a Fernet key
    encrypted_message = encrypt_data(message, fernet_key)  # Encrypt the message

    # Step 2: Encrypt the Fernet key with the recipient's public RSA key
    encrypted_fernet_key = encrypt_fernet_key_with_public_key(fernet_key, recipient_public_key)

    return encrypted_message, encrypted_fernet_key

def decrypt_received_message(encrypted_message, encrypted_fernet_key, recipient_private_key):
    """
    Decrypt the received message from an encrypted format.
    
    Parameters:
    - encrypted_message: The message that was encrypted.
    - encrypted_fernet_key: The Fernet key encrypted with the recipient's public key.
    - recipient_private_key: The private RSA key of the recipient to decrypt the Fernet key.
    
    Returns:
    The decrypted message.
    """
    # Step 1: Decrypt the Fernet key with the recipient's private RSA key
    fernet_key = decrypt_fernet_key_with_private_key(encrypted_fernet_key, recipient_private_key)

    # Step 2: Use the decrypted Fernet key to decrypt the message
    decrypted_message = decrypt_data(encrypted_message, fernet_key)

    return decrypted_message

def send_secure_message(message, recipient_public_key):
    """
    Encrypt a message and prepare it for secure transmission.
    
    Parameters:
    - message (str): The message to be sent securely.
    - recipient_public_key: The recipient's public key for encryption.
    
    Returns:
    Tuple of encrypted message and encrypted Fernet key.
    """
    return encrypt_fernet_key_with_public_key
