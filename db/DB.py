import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from utils.Logger import Logger

log = Logger()


class Database:
    def __init__(self, db_file: str | None):
        """Database class for SQLite3

        Args:
            db_file (str | bytes): String or bytes object pointing to the database file
        """
        self.db_file = db_file if db_file != None else ":memory:"
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.db_file)
        self.conn = None

    def __str__(self):
        return f"Database object for {self.db_file}\n Connection: {self.db.isOpen()}\n"

    def connect(self):
        if not self.db.open():
            log.error(f"Cannot open database: {self.db.lastError().text()}")
            sys.exit(1)
        else:
            self.conn = self.db
            log.info(f"Connected to database: {self.db_file}")

    def close(self):
        if self.db.isOpen():
            self.db.close()
            log.info(f"Closed database: {self.db_file}")

        else:
            log.error(f"Cannot close database: {self.db.lastError().text()}")

    def create_table(self):
        """Create user, seed and project table in the database"""

        query = QSqlQuery()
        query.exec(
            """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL)"""
        )
        query.exec(
            """CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))"""
        )
        query.exec(
            """CREATE TABLE IF NOT EXISTS seeds (id INTEGER PRIMARY KEY AUTOINCREMENT, seed_value TEXT NOT NULL, project_id INTEGER NOT NULL, FOREIGN KEY(project_id) REFERENCES projects(id))"""
        )
