import random, string
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, key):
        self.key = key

    def encrypt_password(self, password):
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(self.key)
        return cipher_suite.decrypt(encrypted_password.encode()).decode()
    
    def generate_strong_password(self, length):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        pass_list = list(password)
        random.shuffle(pass_list)
        return ''.join(pass_list)