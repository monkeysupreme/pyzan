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
            self.commit()

    def insert(self, key, value):
        try:
            self.execute(
                "INSERT OR REPLACE INTO store (key, value) VALUES (?, ?);",
                (key, value)
            )
            self.commit()
        except sqlite3.Error:
            db_log.error("Insert failed")

    def query(self, key):
        try:
            cursor = self.execute(
                "SELECT value FROM store WHERE key = ?;",
                (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except sqlite3.Error:
            db_log.error("Query failed")
            return None

    def delete(self, key):
        try:
            self.execute("DELETE FROM store WHERE key = ?;", (key,))
            self.commit()
        except sqlite3.Error:
            db_log.error("Delete failed")

    def get_all(self):
        try:
            cursor = self.execute("SELECT key, value FROM store;")
            return cursor.fetchall()
        except sqlite3.Error:
            db_log.error("Get all failed")
            return []



