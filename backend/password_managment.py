import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

class PasswordManager:
    def __init__(self, key=None):
        self.key = key

    def encrypt_password(self, password):
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(self.key)
        return cipher_suite.decrypt(encrypted_password.encode()).decode()
    
    def generate_strong_password(self, length):
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!", k=length))
        pass_list = list(password)
        random.shuffle(pass_list)
        return ''.join(pass_list)
    
    @staticmethod
    def derive_key(password, salt):
            if isinstance(password, bytes):
                password = password.decode()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode())
            return urlsafe_b64encode(key)
    
    def set_encryption_key(self, key):
        self.key = key
