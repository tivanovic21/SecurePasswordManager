import bcrypt
import sqlite3

class Authentication:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    
    @staticmethod
    def fetchUser(email):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT email, first_name, last_name FROM User WHERE email=?", (email,))
        user: object = cur.fetchone()
        return user
    
    def login_user(email, password):
        try:
            conn = sqlite3.connect("db.sqlite")
            cur = conn.cursor()

            cur.execute("SELECT master_password FROM User WHERE email=?", (email,))
            data = cur.fetchone()

            if data:
                hashed_password = data[0]
                if Authentication.verify_password(password, hashed_password):
                    user = Authentication.fetchUser(email)
                    return True, user
                else:
                    return False, 'Invalid email or password.'
            else:
                return False, 'Invalid email or password.'

        except sqlite3.Error as e:
            print("Error accessing database:", e)
            return False, 'Error accessing database.'

        finally:
            if conn:
                conn.close()

    def register_user(email, password, fname, lname, twoFA=False, twoFA_secret=None):
        print("Registering user...")
        try:
            conn = sqlite3.connect("db.sqlite")
            cur = conn.cursor()

            hashed_password = Authentication.hash_password(password)

            cur.execute("INSERT INTO User (email, master_password, first_name, last_name, twoFA, twoFA_secret) VALUES (?, ?, ?, ?, ?, ?)", (email, hashed_password, fname, lname, twoFA, twoFA_secret))
            conn.commit()
            return True

        except sqlite3.Error as e:
            print("Error accessing database:", e)
            return False

        finally:
            if conn:
                conn.close()
