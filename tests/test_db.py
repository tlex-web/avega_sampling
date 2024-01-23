# FILEPATH: /c:/programming/avega_sampling/tests/test_db.py

import pytest
from PyQt6.QtSql import QSqlDatabase
from db.DB import Database

from tests.fixtures import setup_database


def test_database_connection(setup_database):
    assert setup_database.db.isOpen()


def test_database_insert(setup_database):
    setup_database.insert("test_table", ("test_value",))
    query = QSqlDatabase.database().exec("SELECT * FROM test_table")
    assert query.value(0) == "test_value"


def test_database_update(setup_database):
    setup_database.insert("test_table", ("test_value",))
    setup_database.update("test_table", ("updated_value",), "column='test_value'")
    query = QSqlDatabase.database().exec(
        "SELECT * FROM test_table WHERE column='updated_value'"
    )
    assert query.value(0) == "updated_value"


def test_database_delete(setup_database):
    setup_database.insert("test_table", ("test_value",))
    setup_database.delete("test_table", "column='test_value'")
    query = QSqlDatabase.database().exec(
        "SELECT * FROM test_table WHERE column='test_value'"
    )
    assert not query.value(0) == "test_value"


def test_database_read(setup_database):
    setup_database.insert("test_table", ("test_value",))
    setup_database.read("test_table", "column", "column='test_value'")
    query = QSqlDatabase.database().exec(
        "SELECT * FROM test_table WHERE column='test_value'"
    )
    assert query.value(0) == "test_value"
