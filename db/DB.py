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

    def insert(self, table: str, values: str | list[str]):
        """Insert values into a table

        Args:
            table (str): Name of the table to insert into
            values (tuple): Values to insert into the table
        """
        query = QSqlQuery()
        query.prepare(f"INSERT INTO {table} VALUES {values}")

        if not query.exec():
            log.error(
                f"Cannot insert values into table {table}: {query.lastError().text()}"
            )
        else:
            log.info(f"Inserted values into table {table}")

    def update(self, table: str, values: tuple, where: str):
        """Update values in a table

        Args:
            table (str): Name of the table to update
            values (tuple): Values to update in the table
            where (str): Where clause to use
        """
        query = QSqlQuery()
        query.prepare(f"UPDATE {table} SET {values} WHERE {where}")
        if not query.exec():
            log.error(
                f"Cannot update values in table {table}: {query.lastError().text()}"
            )
        else:
            log.info(f"Updated values in table {table}")

    def delete(self, table: str, where: str):
        """Delete values from a table

        Args:
            table (str): Name of the table to delete from
            where (str): Where clause to use
        """
        query = QSqlQuery()
        query.prepare(f"DELETE FROM {table} WHERE {where}")
        if not query.exec():
            log.error(
                f"Cannot delete values from table {table}: {query.lastError().text()}"
            )
        else:
            log.info(f"Deleted values from table {table}")

    def read(self, table: str, columns: str, where: str):
        """Read values from a table

        Args:
            table (str): Name of the table to read from
            columns (str): Columns to read from the table
            where (str): Where clause to use
        """
        query = QSqlQuery()
        query.prepare(f"SELECT {columns} FROM {table} WHERE {where}")
        if not query.exec():
            log.error(
                f"Cannot read values from table {table}: {query.lastError().text()}"
            )
        else:
            log.info(f"Read values from table {table}")
