import sqlite3
from sqlite3 import Error

from utils.Logger import Logger

log = Logger()


class Database:
    def __init__(self, db_file: str | bytes | None):
        """Database class for SQLite3

        Args:
            db_file (str | bytes): String or bytes object pointing to the database file
        """
        self.db_file = db_file if db_file else ":memory:"
        self.conn = None

    def __str__(self):
        return f"Database object for {self.db_file}\n Connection: {self.conn}\n Version: {sqlite3.version}\n"

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            log.info(f"Connected to database {self.db_file}")
        except Error as e:
            log.error(e)

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, sql):
        """Executes a SQL statement

        Args:
            sql (str): SQL statement to execute
        """
        if self.conn:
            try:
                c = self.conn.cursor()
                c.execute(sql)
                self.conn.commit()
            except Error as e:
                log.error(e)

    def query(self, sql):
        if self.conn:
            try:
                c = self.conn.cursor()
                c.execute(sql)
                return c.fetchall()
            except Error as e:
                log.error(e)

    def create_table(self, table_name: str, columns: list[str]):
        """Create a table in the database

        Args:
            table_name (str)
            columns (list[str])
        """
        sql = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
        for i in range(len(columns)):
            sql += columns[i]
            if i < len(columns) - 1:
                sql += ","
        sql += ");"
        self.execute(sql)

        log.info(f"Created table {table_name}")

    def insert(self, table_name: str, columns: list[str], values: list[str]):
        """Insert a row into a table

        Args:
            table_name (str): _description_
            columns (list[str]): _description_
            values (list[str]): _description_
        """
        sql = "INSERT INTO " + table_name + " ("
        for i in range(len(columns)):
            sql += columns[i]
            if i < len(columns) - 1:
                sql += ","
        sql += ") VALUES ("
        for i in range(len(values)):
            sql += "'" + values[i] + "'"
            if i < len(values) - 1:
                sql += ","
        sql += ");"
        self.execute(sql)

        log.info(f"Inserted row into table {table_name}")

    def select(self, table_name: str, columns: str | list[str], where: str):
        """Select rows from a table

        Args:
            table_name (str): _description_
            columns (str | list[str]): _description_
            where (str): _description_

        Returns:
            _type_: _description_
        """
        sql = "SELECT "
        for i in range(len(columns)):
            sql += columns[i]
            if i < len(columns) - 1:
                sql += ","
        sql += " FROM " + table_name + " WHERE " + where + ";"
        return self.query(sql)

    def update(
        self, table_name: str, columns: list[str], values: list[str], where: str
    ):
        """Update rows in a table

        Args:
            table_name (str): _description_
            columns (list[str]): _description_
            values (list[str]): _description_
            where (str): _description_
        """

        sql = "UPDATE " + table_name + " SET "
        for i in range(len(columns)):
            sql += columns[i] + "='" + values[i] + "'"
            if i < len(columns) - 1:
                sql += ","
        sql += " WHERE " + where + ";"
        self.execute(sql)

        log.info(f"Updated row in table {table_name}")

    def delete(self, table_name: str, where: str):
        """Delete rows from a table

        Args:
            table_name (str): _description_
            where (str): _description_
        """
        sql = "DELETE FROM " + table_name + " WHERE " + where + ";"
        self.execute(sql)

        log.info(f"Deleted row from table {table_name}")

    def drop_table(self, table_name: str):
        """Drop a table from the database

        Args:
            table_name (str): _description_
        """
        sql = "DROP TABLE " + table_name + ";"
        self.execute(sql)

        log.info(f"Dropped table {table_name}")
