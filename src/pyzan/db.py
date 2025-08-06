import sqlite3
import os


from pyzan.log import Logger


db_log = Logger(module="DB", log_file="logs/db.log")


class Database(sqlite3.Connection):
    def __init__(self, file: str) -> None:
        self.did_exist = os.path.exists(file)
        super().__init__(database=file)
        self.file = file

        self.is_new: bool = not self.did_exist

        if self.is_new:
            self.execute("CREATE TABLE store (key TEXT PRIMARY KEY, value TEXT);")

    def insert(self, key, value):
        self.execute(
            "INSERT INTO store (key, value) VALUES (?, ?);",
            (key, value)
        )

    def query(self, key):
        row = self.execute(
            "SELECT value FROM store WHERE key = ?",
            (key,)
        ).fetchone()

        return row[0] if row else None

    def delete(self, key):
        self.execute("DELETE FROM store WHERE key = ?", (key,))

    def get_all(self):
        cursor = self.execute("SELECT key, value FROM store;")
        return cursor.fetchall()
