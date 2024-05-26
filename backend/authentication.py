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
        cur.execute("SELECT username from User where email=?", (email,))
        user: object = cur.fetchone()
        return user

    @staticmethod
    def checkDB():
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT * FROM User")
        user = cur.fetchall()
        conn.close()
        if len(user) == 0:
            return True
        else:
            return False
    
    @staticmethod
    def fetchUserData():
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT * from User")
        user = cur.fetchone()
        conn.close()
        if user:
            return user
        
    @staticmethod
    def getSalt(): 
        conn, curr = Authentication.connectDB()
        curr.execute("SELECT salt from User where id=1")
        salt = curr.fetchone()
        conn.close()
        return salt
        
    @staticmethod
    def updateFingerprint(status):
        conn, cur = Authentication.connectDB()
        id = Authentication.fetchUserData()[0]
        if status == 1:
            cur.execute("UPDATE User SET fingerprint = 0 WHERE id=?", (id,))
        else:
            cur.execute("UPDATE User SET fingerprint = 1 WHERE id=?", (id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update2FA(status):
        conn, cur = Authentication.connectDB()
        id = Authentication.fetchUserData()[0]
        firstTime = False

        if status == 1:
            cur.execute("UPDATE User SET twoFA = 0 WHERE id=?", (id,)) #turn off 2fa
        else:
            cur.execute("UPDATE User SET twoFA = 1 WHERE id=?", (id,)) #turn on 2fa
            twoFA_secret = Authentication.fetchUserData()[5]
            if twoFA_secret is None:
                firstTime = True
                twoFA_secret = TwoFactorAuth.generateSecret()
                cur.execute("UPDATE User SET twoFA_secret=? WHERE id=?", (twoFA_secret, id))
            else: 
                firstTime = False
        
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
        else:
            return False
        
    @staticmethod
    def saveNewPassword(email, password):
        conn, cur = Authentication.connectDB()
        hashed_password = Authentication.hash_password(password)
        cur.execute("UPDATE User SET master_password=?, token=NULL, token_expiration=NULL WHERE email=?", (hashed_password, email))
        conn.commit()
        conn.close()

    def login_user(password):
        try:
            data = Authentication.fetchUserData()

            if data:
                hashed_password = data[2]
                if Authentication.verify_password(password, hashed_password):
                    user = Authentication.fetchUser(data[1])
                    encoded_salt = data[9]
                    salt = base64.b64decode(encoded_salt)
                    if salt:
                        encryption_key = PasswordManager.derive_key(password, salt)
                        PasswordManager.set_encryption_key(PasswordManager, encryption_key)
                    return True, user[0]
                else:
                    return False, 'Invalid password.'
            else:
                return False, 'Invalid password.'

        except sqlite3.Error as e:
            print("Error accessing database:", e)
            return False, 'Error accessing database.'

    def register_user(email, password, username, twoFA=False, twoFA_secret=None, fingerprint=False, salt=''):
        if Authentication.checkDB():
            try:
                conn, cur = Authentication.connectDB()
                hashed_password = Authentication.hash_password(password)
                salt = os.urandom(16)
                encoded_salt = base64.b64encode(salt).decode('utf-8') #convert bytes to string to fit VARCHAR

                cur.execute("INSERT INTO User (email, master_password, username, twoFA, twoFA_secret, fingerprint, salt) VALUES (?, ?, ?, ?, ?, ?, ?)", (email, hashed_password, username, twoFA, twoFA_secret, fingerprint, encoded_salt))
                conn.commit()

                encryption_key = PasswordManager.derive_key(password, salt)
                PasswordManager.set_encryption_key(PasswordManager, encryption_key)

                return True, f'Registered successfully as {username}'

            except sqlite3.Error as e:
                print("Error accessing database:", e)
                return False, 'Error accessing database.'

            finally:
                if conn:
                    conn.close()
        else:
            return False, 'Only one user can be registered.'