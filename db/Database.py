import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from utils.Logger import log, LogEnvironment
from config import DB_TYPE


class Database:
    def __init__(self, db_file=None):
        """Database class for SQLite3

        Args:
            db_file (str, optional): Path to the database file. Defaults to None.
        """
        self.db_file = db_file if db_file is not None else ":memory:"
        self.db = QSqlDatabase.addDatabase(DB_TYPE)
        self.db.setDatabaseName(self.db_file)
        self.conn = None

    def __str__(self):
        return f"Database object for {self.db_file}\n Connection: {self.db.isOpen()}\n"

    def connect(self):
        if not self.db.open():
            log.error(
                f"Cannot open database: {self.db.lastError().text()}",
                LogEnvironment.DATABASE,
            )
            sys.exit(1)
        else:
            self.conn = self.db
            log.info(f"Connected to database: {self.db_file}", LogEnvironment.DATABASE)

    def close(self):
        if self.db.isOpen():
            self.db.close()
            log.info(f"Closed database: {self.db_file}", LogEnvironment.DATABASE)

        else:
            log.error(
                f"Cannot close database: {self.db.lastError().text()}",
                LogEnvironment.DATABASE,
            )

    def create_tables(self):
        """Create user, seed and project table in the database"""

        query = QSqlQuery()
        if query.exec(
            """CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(username) ON CONFLICT FAIL)"""
        ):
            log.info("Created table: users", LogEnvironment.DATABASE)
        else:
            log.error(
                f"Failed to create table: users {query.lastError().text()}",
                LogEnvironment.DATABASE,
            )
        if query.exec(
            """CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))"""
        ):
            log.info("Created table: projects", LogEnvironment.DATABASE)
        else:
            log.error(
                f"Failed to create table: projects {query.lastError().text()}",
                LogEnvironment.DATABASE,
            )
        if query.exec(
            """CREATE TABLE IF NOT EXISTS seeds (seed_id INTEGER PRIMARY KEY AUTOINCREMENT, seed_value INTEGER NOT NULL, user_id INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))"""
        ):
            log.info("Created table: seeds", LogEnvironment.DATABASE)
        else:
            log.error(
                f"Failed to create table: seeds {query.lastError().text()}",
                LogEnvironment.DATABASE,
            )

    def drop_table(self, table_name: str):
        """Drop a table from the database

        Args:
            table_name (str): Name of the table to drop
        """

        query = QSqlQuery()
        query.exec(f"DROP TABLE {table_name}")

        log.info(f"Dropped table: {table_name}", LogEnvironment.DATABASE)

    def clear_table(self, table_name: str):
        """Clear a table from the database

        Args:
            table_name (str): Name of the table to clear
        """

        query = QSqlQuery()
        query.exec(f"DELETE FROM {table_name}")

        log.info(f"Cleared table: {table_name}", LogEnvironment.DATABASE)
