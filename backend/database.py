import sqlite3
from backend.authentication import Authentication

class PasswordDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS passwords (
                            id INTEGER PRIMARY KEY,
                            website TEXT,
                            username TEXT,
                            password TEXT
                            )''')
        self.conn.commit()

    def insert_password(self, website, username, password):
        self.cur.execute("INSERT INTO Password (website, username, password) VALUES (?, ?, ?)",
                          (website, username, password))
        self.conn.commit()

    def get_all_passwords(self):
        self.cur.execute("SELECT * FROM Password")
        return self.cur.fetchall()

    def delete_password(self, password_id):
        conn, cur = Authentication.connectDB()
        cur.execute("DELETE FROM Password WHERE id=?", (password_id,))
        conn.commit()
        conn.close()

    def close(self):
        self.conn.close()

    # CRUD operations for Password and Application tables

    def get_app_id(self, app_name):
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT id FROM Application WHERE app_name=?", (app_name,))
        app_id = cur.fetchone()[0]
        conn.close()
        return app_id

    def get_pass_id(self, values):
        conn, cur = Authentication.connectDB()
        cur.execute("SELECT id FROM Password WHERE username=? AND password=?", (values["username"], values["password"]))
        password_id = cur.fetchone()[0]
        conn.close()
        return password_id

    def get_user_passwords(self, user_id):
        conn, cur = Authentication.connectDB()
        cur.execute("""
            SELECT p.username, p.password, a.app_name, a.domain
            FROM Password p
            JOIN Application a ON p.Application_id = a.id
            WHERE p.User_id = ?
        """, (user_id,))
        passwords = cur.fetchall()
        conn.close()
        return passwords

    def add_password(self, user_id, app_id, username, password):
        print("--- ADD PASS FUNKCIJA ---")
        conn, cur = Authentication.connectDB()
        cur.execute("""
            INSERT INTO Password (User_id, Application_id, username, password)
            VALUES (?, ?, ?, ?)
        """, (user_id, app_id, username, password))
        conn.commit()
        conn.close()

    def update_password(self, password_id, updated_data):
        conn, cur = Authentication.connectDB()
        cur.execute(""" 
            UPDATE Application
            SET app_name=?, domain=?
            WHERE id=?
        """, (updated_data["app_name"], updated_data["domain"], updated_data["app_id"]))
        cur.execute("""
            UPDATE Password
            SET username=?, password=?, Application_id=?
            WHERE id=?
        """, (updated_data["username"], updated_data["password"], updated_data["app_id"], password_id))
        conn.commit()
        conn.close()



    def add_app(self, app_name, domain, user_id):
        conn, cur = Authentication.connectDB()
        cur.execute("INSERT INTO Application (app_name, domain, User_id) VALUES (?, ?, ?)", (app_name, domain, user_id))
        conn.commit()
        app_id = cur.lastrowid
        conn.close()
        return app_id

    def check_app_exists(self, app_name, domain, user_id):
        conn, cur = Authentication.connectDB()
        cur.execute("""
            SELECT id FROM Application
            WHERE app_name=? AND domain=? AND User_id=?
        """, (app_name, domain, user_id))
        website = cur.fetchone()
        conn.close()
        return website[0] if website else None
