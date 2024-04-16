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
