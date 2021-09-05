import sqlite3
from typing import Optional

db_path = './db_sqllite/ccal_db.db'


class UserBD:

    __instance = None
    ccal_db_tables = {
        'users_table': 'users',
        'data_table': 'personal_data',
        'food_table': 'list_of_food',
    }
    active_users = []

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.cursor: Optional[sqlite3.Cursor] = None
        self.sqlite_connection: Optional[sqlite3.Connection] = None

    def __enter__(self):
        self.sqlite_connection = sqlite3.connect(db_path)
        self.cursor = self.sqlite_connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.sqlite_connection.close()

    def get_users_telegram_ids(self):
        with UserBD() as cur:
            cur.execute('SELECT * FROM `users`')
            result = [fields[1] for fields in cur.fetchall()]
            self.active_users += result


if __name__ == '__main__':
    # con = sqlite3.connect(db_path)
    # cursor = con.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall())
    # cursor.close()
    # con.close()
    a = UserBD()
    a.get_users_telegram_ids()
    print(a.active_users)


