import bcrypt
import sqlite3

class Authentication:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    
    @staticmethod
    def fetchUser(email):
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT username from User where email=?", (email,))
        user: object = cur.fetchone()
        return user

    @staticmethod
    def checkDB():
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT * FROM User")
        user = cur.fetchall()
        conn.close()
        if len(user) != 0:
            return False
        else:
            return True
    
    def login_user(password):
        try:
            conn = sqlite3.connect("db.sqlite")
            cur = conn.cursor()

            cur.execute("SELECT * FROM User WHERE id=1")
            data = cur.fetchone()

            if data:
                hashed_password = data[2]
                if Authentication.verify_password(password, hashed_password):
                    user = Authentication.fetchUser(data[1])
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

    def register_user(email, password, username, twoFA=False, twoFA_secret=None, fingerprint=False):
        if Authentication.checkDB():
            try:
                conn = sqlite3.connect("db.sqlite")
                cur = conn.cursor()

                hashed_password = Authentication.hash_password(password)

                cur.execute("INSERT INTO User (email, master_password, username, twoFA, twoFA_secret, fingerprint) VALUES (?, ?, ?, ?, ?, ?)", (email, hashed_password, username, twoFA, twoFA_secret, fingerprint))
                conn.commit()
                return True

            except sqlite3.Error as e:
                print("Error accessing database:", e)
                return False

            finally:
                if conn:
                    conn.close()
        else:
            return False