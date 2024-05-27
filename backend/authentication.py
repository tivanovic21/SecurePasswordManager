import base64
import os
import bcrypt
import sqlite3
from backend.twoFA import TwoFactorAuth
from datetime import datetime
from backend.password_managment import PasswordManager

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
    def connectDB():
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        return conn, cur
    
    @staticmethod
    def fetchUser(email):
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT username FROM User WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()
        return user

    @staticmethod
    def checkDB():
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT * FROM User")
        user = cur.fetchall()
        conn.close()
        return len(user) == 0
    
    @staticmethod
    def fetchUserData():
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT * FROM User")
        user = cur.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def getSalt(): 
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT salt FROM User WHERE id=1")
        salt = cur.fetchone()
        conn.close()
        return salt
    
    @staticmethod
    def updateFingerprint(status):
        conn, cur = Authentication.connectDB()
        id = Authentication.fetchUserData()[0]
        new_status = 0 if status == 1 else 1
        cur.execute("UPDATE User SET fingerprint=? WHERE id=?", (new_status, id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update2FA(status):
        conn, cur = Authentication.connectDB()
        id = Authentication.fetchUserData()[0]
        firstTime = False

        if status == 1:
            cur.execute("UPDATE User SET twoFA=0 WHERE id=?", (id,)) # Turn off 2FA
        else:
            cur.execute("UPDATE User SET twoFA=1 WHERE id=?", (id,)) # Turn on 2FA
            twoFA_secret = Authentication.fetchUserData()[5]
            if twoFA_secret is None:
                firstTime = True
                twoFA_secret = TwoFactorAuth.generateSecret()
                cur.execute("UPDATE User SET twoFA_secret=? WHERE id=?", (twoFA_secret, id))
        
        conn.commit()
        conn.close()
        return firstTime
    
    @staticmethod
    def saveTokenExpiration(email, token, expiration):
        conn, cur = Authentication.connectDB()
        cur.execute("UPDATE User SET token=?, token_expiration=? WHERE email=?", (token, expiration, email))
        conn.commit()
        conn.close()

    @staticmethod
    def checkToken(email, token):
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT token, token_expiration FROM User WHERE email=?", (email,))
        userToken, userExpiration = cur.fetchone()
        conn.close()

        if token == userToken and datetime.now() <= datetime.strptime(userExpiration, '%Y-%m-%d %H:%M:%S.%f'):
            return True
        return False
        
    @staticmethod
    def saveNewPassword(email, password):
        conn, cur = Authentication.connectDB()
        hashed_password = Authentication.hash_password(password)
        cur.execute("UPDATE User SET master_password=?, token=NULL, token_expiration=NULL WHERE email=?", (hashed_password, email))
        conn.commit()
        conn.close()

    @staticmethod
    def login_user(password):
        try:
            data = Authentication.fetchUserData()

            # Debugging: print the data
            # print(f"Retrieved data: {data}")

            if data:
                # Ensure that the data has at least 10 elements
                if len(data) < 10:
                    print("Error: Retrieved data does not have enough elements")
                    return False, 'Invalid user data.'

                hashed_password = data[2]
                if Authentication.verify_password(password, hashed_password):
                    user = Authentication.fetchUser(data[1])
                    encoded_salt = data[9]  # Use index 9 for the salt

                    # Decode the salt and verify
                    try:
                        salt = base64.b64decode(encoded_salt)
                        if salt:
                            encryption_key = PasswordManager.derive_key(password, salt)
                            pm = PasswordManager()
                            pm.set_encryption_key(encryption_key)
                        return True, user[0]
                    except Exception as e:
                        print("Error decoding salt:", e)
                        return False, 'Error decoding salt.'
                else:
                    return False, 'Invalid password.'
            else:
                return False, 'Invalid user data.'

        except sqlite3.Error as e:
            print("Error accessing database:", e)
            return False, 'Error accessing database.'

    @staticmethod
    def register_user(email, password, username, twoFA=False, twoFA_secret=None, fingerprint=False, salt=''):
        if Authentication.checkDB():
            try:
                conn, cur = Authentication.connectDB()
                hashed_password = Authentication.hash_password(password)
                salt = os.urandom(16)
                encoded_salt = base64.b64encode(salt).decode('utf-8')  # Convert bytes to string to fit VARCHAR

                cur.execute("INSERT INTO User (email, master_password, username, twoFA, twoFA_secret, fingerprint, salt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (email, hashed_password, username, twoFA, twoFA_secret, fingerprint, encoded_salt))
                conn.commit()

                encryption_key = PasswordManager.derive_key(password, salt)
                pm = PasswordManager()
                pm.set_encryption_key(encryption_key)

                return True, f'Registered successfully as {username}'

            except sqlite3.Error as e:
                print("Error accessing database:", e)
                return False, 'Error accessing database.'

            finally:
                if conn:
                    conn.close()
        else:
            return False, 'Only one user can be registered.'

# Testing the login functionality
#result, message = Authentication.login_user("correct_password")
#print(result, message)
