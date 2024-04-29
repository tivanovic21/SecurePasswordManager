import random, string
from cryptography.fernet import Fernet
from backend.authentification import Authentication

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
    
    def get_user_passwords(self, user_id):
        conn, cur = Authentication.connectDB()
        cur.execute("""
            SELECT p.password, w.name
            FROM Password p
            JOIN Websites w ON p.Websites_id = w.id
            WHERE p.User_id = ?
        """, (user_id,))
        passwords = cur.fetchall()
        conn.close()
        return passwords

    def add_password(self, user_id, website_id, password):
        conn, cur = Authentication.connectDB()
        cur.execute("""
            INSERT INTO Password (password, User_id, Websites_id)
            VALUES (?, ?, ?)
        """, (password, user_id, website_id))
        conn.commit()
        conn.close()

    def add_website(self, user_id, website_name, domain):
        conn, cur = Authentication.connectDB()
        cur.execute("""
            INSERT INTO Websites (name, User_id, domain)
            VALUES (?, ?)
        """, (website_name, user_id, domain))
        conn.commit()
        conn.close()