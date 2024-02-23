from PyQt6.QtSql import QSqlQuery

from models.User import User
from tests.fixtures import setup_database


def test_create_user(setup_database):
    db = setup_database
    db.connect()

    user = User()
    username = "test_user_create"
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO users (username) VALUES (?)")
    query_insert.addBindValue(username)
    query_insert.exec()

    user_id = query_insert.lastInsertId()
    assert user.read_user(user_id) == {"user_id": user_id, "username": username}


def test_read_user(setup_database):
    db = setup_database
    db.connect()

    user = User()
    username = "test_user_read"
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO users (username) VALUES (?)")
    query_insert.addBindValue(username)
    query_insert.exec()

    query = user.read_user(query_insert.lastInsertId())
    assert query is not None
    assert query["username"] == username


def test_update_user(setup_database):
    db = setup_database
    db.connect()

    user = User()
    username = "test_user_update"
    new_username = "updated_user"
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO users (username) VALUES (?)")
    query_insert.addBindValue(username)
    query_insert.exec()

    user_id = query_insert.lastInsertId()
    assert user.update_user(user_id, new_username)

    query = QSqlQuery()
    query.exec(f"SELECT * FROM users WHERE user_id = {user_id}")
    assert query.next()
    assert query.value("username") == new_username


def test_delete_user(setup_database):
    db = setup_database
    db.connect()

    user = User()
    username = "test_user_delete"
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO users (username) VALUES (?)")
    query_insert.addBindValue(username)
    query_insert.exec()

    user_id = query_insert.lastInsertId()
    assert user.delete_user(user_id)

    query = QSqlQuery()
    query.exec(f"SELECT * FROM users WHERE user_id = {user_id}")
    assert not query.next()
