import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')


class DatabaseManagement:
    def __init__(self):
        self.db = psycopg2.connect(DATABASE_URL, sslmode='require')

    def insert_user(self, email, display_name, password, previous_passwords_list):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""INSERT INTO users (email, display_name, password, previous_passwords_list) 
                VALUES (%s, %s, %s, %s)""", (email, display_name, password, previous_passwords_list))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def update_user(self, email, password, previous_passwords_list, reset_password_next_login):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""UPDATE users SET password=%s, previous_passwords_list=%s, reset_password_next_login=%s 
                WHERE email=%s""", (password, previous_passwords_list, reset_password_next_login, email))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def update_user_forgot_password(self, email, password, reset_password_next_login):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""UPDATE users SET password=%s, reset_password_next_login=%s WHERE email=%s""",
                        (password, reset_password_next_login, email))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def get_user_by_email(self, email):
        try:
            cur = self.db.cursor()
            query = """SELECT id, password, locked, reset_password_next_login, previous_passwords_list, is_admin, 
                display_name FROM users WHERE email=%s"""
            cur.execute(query, (email,))
            result = cur.fetchall()
            return result
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def get_user_by_uid(self, uid):
        try:
            cur = self.db.cursor()
            query = """SELECT email, display_name, is_admin FROM users WHERE id=%s"""
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

    def get_users(self):
        try:
            cur = self.db.cursor()
            cur.execute("SELECT email, display_name, locked FROM users ORDER BY email")
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
            cur.execute("""INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)""", (name, phone, address))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def get_login_attempts(self, email):
        try:
            cur = self.db.cursor()
            query = """SELECT login_retries from users WHERE email=%s"""
            cur.execute(query, (email,))
            result = cur.fetchall()
            return result
        except psycopg2.DatabaseError as error:
            result = error
        finally:
            if cur is not None:
                cur.close()

        return result

    def update_login_attempts(self, login_attempts, email):
        result = 0
        try:
            cur = self.db.cursor()
            cur.execute("""UPDATE users SET login_retries=%s WHERE email=%s""", (login_attempts, email))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def lock_user(self, email):
        result = 0
        try:
            cur = self.db.cursor()
            query = """UPDATE users SET locked=1 WHERE email=%s"""
            cur.execute(query, (email,))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def unlock_user(self, email):
        result = 0
        try:
            cur = self.db.cursor()
            query = """UPDATE users SET login_retries=0, locked=0 WHERE email=%s"""
            cur.execute(query, (email,))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def delete_user(self, email):
        result = 0
        try:
            cur = self.db.cursor()
            query = """DELETE FROM users WHERE email=%s"""
            cur.execute(query, (email,))
            self.db.commit()
        except psycopg2.DatabaseError as error:
            result = error
            cur.execute("rollback")
            self.db.commit()
        finally:
            if cur is not None:
                cur.close()

        return result

    def __del__(self):
        self.db.close()
