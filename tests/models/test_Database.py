import pytest
from PyQt6.QtSql import QSqlQuery

from fixtures import setup_database


def test_connect(setup_database):
    db = setup_database
    assert db.conn is not None
    assert db.db.isOpen()


def test_close(setup_database):
    db = setup_database
    db.close()
    assert not db.db.isOpen()


def test_create_tables(setup_database):
    db = setup_database
    query = QSqlQuery()
    query.exec("SELECT name FROM sqlite_master WHERE type='table'")
    tables = []
    while query.next():
        tables.append(query.value(0))
    assert "users" in tables
    assert "projects" in tables
    assert "seeds" in tables


def test_drop_table(setup_database):
    db = setup_database
    db.drop_table("users")
    query = QSqlQuery()
    query.exec("SELECT name FROM sqlite_master WHERE type='table'")
    tables = []
    while query.next():
        tables.append(query.value(0))
    assert "users" not in tables


def test_clear_table(setup_database):
    db = setup_database
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO users (username) VALUES (?)")
    query_insert.addBindValue("test_user")
    query_insert.exec()
    db.clear_table("users")
    query_select = QSqlQuery()
    query_select.exec("SELECT * FROM users")
    assert not query_select.next()
