import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')


class DatabaseManagement:
    def __init__(self):
        self.db = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.db.cursor()

    def get_users_count(self):
        self.cursor.execute("SELECT count(*) FROM users")
        result = self.cursor.fetchall()[0][0]
        return result

    def insert_user(self, email, password):
        self.cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s)""",
                            (email, password))
        self.db.commit()

    def update_user(self, email, password, reset_password_next_login):
        self.cursor.execute("""UPDATE users SET password=%s, reset_password_next_login=%s WHERE email=%s""",
                            (password, reset_password_next_login, email))
        self.db.commit()

    def get_user_by_email(self, email):
        query = """SELECT id, password, locked FROM users WHERE email=%s"""
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchall()
        return result

    def get_user_by_uid(self, uid):
        query = """SELECT email FROM users WHERE id=%s"""
        self.cursor.execute(query, (uid,))
        result = self.cursor.fetchall()
        return result

    def get_customers(self):
        self.cursor.execute("SELECT * FROM customers ORDER BY name")
        result = self.cursor.fetchall()
        return result

    def get_specific_user_by_email(self, email):
        query = """SELECT email FROM users WHERE email=%s"""
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchall()
        return result

    def insert_customer(self, name, address, phone):
        self.cursor.execute("""INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)""",
                            (name, address, phone))
        self.db.commit()

    def __del__(self):
        self.cursor.close()
        self.db.close()
