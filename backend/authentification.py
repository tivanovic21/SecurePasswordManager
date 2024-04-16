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
        return bcrypt.checkpw(plain_password.encode(), hashed_password)
    
    def login_user(email, password):
        print("Authenticating user...")
        try:
            conn = sqlite3.connect("db.sqlite")
            cur = conn.cursor()

            # Query the User table for the provided email
            cur.execute("SELECT password_hash FROM User WHERE email=?", (email,))
            user_record = cur.fetchone()

            if user_record:
                # Extract the hashed password from the retrieved record
                hashed_password = user_record[0]

                # Verify the provided password against the hashed password
                if Authentication.verify_password(password, hashed_password):
                    return True  # Authentication successful
                else:
                    return False  # Incorrect password
            else:
                return False  # User does not exist

        except sqlite3.Error as e:
            print("Error accessing database:", e)
            return False  # Error occurred

        finally:
            if conn:
                conn.close()

