import random, string
from cryptography.fernet import Fernet
from backend.authentication import Authentication

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
        print("--- ADD PASS FUNKCIJA ---")
        print("user_id: ", user_id, "website_id: ", website_id, "password: ", password)
        conn, cur = Authentication.connectDB()
        cur.execute("""
            INSERT INTO Password (User_id, Websites_id, password)
            VALUES (?, ?, ?)
        """, (user_id, website_id, password))
        conn.commit()
        conn.close()

    def add_website(self, website_name, domain, user_id):
        conn, cur = Authentication.connectDB()
        cur.execute("INSERT INTO Websites (name, domain, User_id) VALUES (?, ?, ?)", (website_name, domain, user_id))
        conn.commit()
        website_id = cur.lastrowid
        conn.close()
        return website_id

    def check_website_exists(self, website_name, domain, user_id):
        conn, cur = Authentication.connectDB()
        cur.execute("""
            SELECT id FROM Websites
            WHERE name=? AND domain=? AND User_id=?
        """, (website_name, domain, user_id))
        website = cur.fetchone()
        conn.close()
        return website[0] if website else None