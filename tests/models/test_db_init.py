from PyQt6.QtSql import QSqlQuery

from tests.fixtures import setup_database


def test_database_connect(setup_database):
    db = setup_database
    db.connect()
    assert db.conn is not None
    assert db.db.isOpen()


def test_database_close(setup_database):
    db = setup_database
    db.connect()
    db.close()
    assert not db.db.isOpen()


def test_database_create_table(setup_database):
    db = setup_database
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
