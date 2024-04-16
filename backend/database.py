import sqlite3

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
        self.cur.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                          (website, username, password))
        self.conn.commit()

    def get_all_passwords(self):
        self.cur.execute("SELECT * FROM passwords")
        return self.cur.fetchall()

    def delete_password(self, password_id):
        self.cur.execute("DELETE FROM passwords WHERE id=?", (password_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
