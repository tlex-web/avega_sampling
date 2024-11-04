import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from library.Logger import log, LogEnvironment
from config import DB_TYPE


def read_sql_file(file_path: str) -> str:
    """Read SQL file and return the content as a string

    Args:
        file_path (str): Path to the SQL file

    Returns:
        str: Content of the SQL file
    """

    with open(file_path, "r") as file:
        return file.read()


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

        sql_database_schema = read_sql_file("db/schema.sql")
        queries = sql_database_schema.split(";")

        for query_text in queries:
            query_text = query_text.strip()
            if query_text:
                query = QSqlQuery()
                if query.exec(query_text):
                    log.info(f"Executed query: {query_text}", LogEnvironment.DATABASE)
                else:
                    log.error(
                        f"Failed to execute query: {query_text} {query.lastError().text()}",
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
