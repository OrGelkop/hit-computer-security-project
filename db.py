import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class DatabaseManagement:
    def __init__(self):
        self.db = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.db.cursor()

    def get_users_count(self):
        self.cursor.execute("SELECT count(*) FROM users")
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.cursor.close()
        self.db.close()
