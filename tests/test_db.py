# FILEPATH: /c:/programming/avega_sampling/tests/test_db.py

import pytest
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from db.DB import Database

from tests.fixtures import setup_database


def test_database_connection(setup_database):
    assert setup_database.db.isOpen()


def test_database_insert(setup_database):

    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO test_table (name) VALUES (?)")
    query_insert.addBindValue("test_value")

    res, id = setup_database.insert(query_insert)

    query = setup_database.read(f"SELECT * FROM test_table WHERE id = {id}")

    assert query.value(0) == "test_value"


def test_database_read(setup_database):
    setup_database.create_table("test_table")
    setup_database.insert("test_table", "test_value")
    setup_database.read("test_table", "column", "column='test_value'")
    query = QSqlDatabase.database().exec(
        "SELECT * FROM test_table WHERE column='test_value'"
    )
    assert query.value(0) == "test_value"


def test_database_update(setup_database):
    setup_database.create_table("test_table")
    setup_database.insert("test_table", "test_value")
    setup_database.update("test_table", ("updated_value",), "column='test_value'")
    query = QSqlDatabase.database().exec(
        "SELECT * FROM test_table WHERE column='updated_value'"
    )
    assert query.value(0) == "updated_value"


def test_database_delete(setup_database):
    setup_database.create_table("test_table")
    setup_database.insert("test_table", "test_value")
    setup_database.delete("test_table", "column='test_value'")
    query = QSqlDatabase.database().exec(
        "SELECT * FROM test_table WHERE column='test_value'"
    )
    assert not query.value(0) == "test_value"
