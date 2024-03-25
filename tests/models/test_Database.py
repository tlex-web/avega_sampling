import pytest
from unittest.mock import MagicMock
from PyQt6.QtSql import QSqlQuery

from db.Database import Database


@pytest.fixture
def database():
    return Database(":memory:")


def test_connect(database):
    database.db.open = MagicMock(return_value=True)
    database.connect()
    assert database.conn == database.db
    assert database.db.open.called


def test_connect_failure(database):
    database.db.open = MagicMock(return_value=False)
    with pytest.raises(SystemExit):
        database.connect()
    assert not database.db.open.called


def test_close(database):
    database.db.isOpen = MagicMock(return_value=True)
    database.close()
    assert database.db.close.called


def test_close_failure(database):
    database.db.isOpen = MagicMock(return_value=False)
    database.close()
    assert not database.db.close.called


def test_database_create_table(database):
    db = database
    db.connect()
    db.create_tables()

    query = QSqlQuery()
    query.exec("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert query.next()
    assert query.value(0) == "users"

    query.exec("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
    assert query.next()
    assert query.value(0) == "projects"

    query.exec("SELECT name FROM sqlite_master WHERE type='table' AND name='seeds'")
    assert query.next()
    assert query.value(0) == "seeds"


def test_drop_table(database):
    database.query = MagicMock()
    table_name = "users"
    database.drop_table(table_name)
    assert database.query.exec.called_with(f"DROP TABLE {table_name}")


def test_clear_table(database):
    database.query = MagicMock()
    table_name = "users"
    database.clear_table(table_name)
    assert database.query.exec.called_with(f"DELETE FROM {table_name}")
