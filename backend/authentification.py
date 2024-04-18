import bcrypt
import sqlite3
from backend.twoFA import TwoFactorAuth
from datetime import datetime

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
            conn, cur = Authentication.connectDB()

            cur.execute("SELECT * FROM User WHERE id=1")
            data = cur.fetchone()

            if data:
                hashed_password = data[2]
                if Authentication.verify_password(password, hashed_password):
                    user = Authentication.fetchUser(data[1])
                    return True, user[0]
                else:
                    return False, 'Invalid password.'
            else:
                return False, 'Invalid password.'

        except sqlite3.Error as e:
            print("Error accessing database:", e)
            return False, 'Error accessing database.'

        finally:
            if conn:
                conn.close()

    def register_user(email, password, username, twoFA=False, twoFA_secret=None, fingerprint=False):
        if Authentication.checkDB():
            try:
                conn, cur = Authentication.connectDB()
                hashed_password = Authentication.hash_password(password)

                cur.execute("INSERT INTO User (email, master_password, username, twoFA, twoFA_secret, fingerprint) VALUES (?, ?, ?, ?, ?, ?)", (email, hashed_password, username, twoFA, twoFA_secret, fingerprint))
                conn.commit()
                return True, f'Registered successfully as {username}'

            except sqlite3.Error as e:
                print("Error accessing database:", e)
                return False, 'Error accessing database.'

            finally:
                if conn:
                    conn.close()
        else:
            return False, 'Only one user can be registered.'