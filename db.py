import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')


class DatabaseManagement:
    def __init__(self):
        self.db = psycopg2.connect(DATABASE_URL, sslmode='require')

    def insert_user(self, email, password, previous_passwords_list):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""INSERT INTO users (email, password, previous_passwords_list) VALUES (%s, %s, %s)""",
                        (email, password, previous_passwords_list))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def update_user(self, email, password, previous_passwords_list, reset_password_next_login):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""UPDATE users SET password=%s, previous_passwords_list=%s, reset_password_next_login=%s WHERE email=%s""",
                        (password, previous_passwords_list, reset_password_next_login, email))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def get_user_by_email(self, email):
        try:
            cur = self.db.cursor()
            query = """SELECT id, password, locked, previous_passwords_list FROM users WHERE email=%s"""
            cur.execute(query, (email,))
            result = cur.fetchall()
            return result
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def get_user_email_by_uid(self, uid):
        try:
            cur = self.db.cursor()
            query = """SELECT email FROM users WHERE id=%s"""
            cur.execute(query, (uid,))
            result = cur.fetchall()
            return result
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def get_customers(self):
        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM customers ORDER BY name")
            result = cur.fetchall()
            return result
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def insert_customer(self, name, address, phone):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)""", (name, address, phone))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def __del__(self):
        self.db.close()
