import pytest_mock
from PyQt6.QtSql import QSqlQuery


from fixtures import user

mocker = pytest_mock.mocker


def test_create_user(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "lastInsertId", return_value=1)

    username = "test_user"

    result = user.create_user(username)

    assert result == 1
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.lastInsertId.assert_called_once_with()


def test_read_user_id_existing(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=True)
    mocker.patch.object(QSqlQuery, "value", side_effect=[1, "test_user"])

    user_id = 1

    result = user.read_user_id(user_id)

    assert result == {
        "user_id": 1,
        "username": "test_user",
    }
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()
    QSqlQuery.value.assert_any_call("user_id")
    QSqlQuery.value.assert_any_call("username")


def test_read_user_id_non_existing(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=False)

    user_id = 1

    result = user.read_user_id(user_id)

    assert result is None
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()


def test_read_user_username_existing(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=True)
    mocker.patch.object(QSqlQuery, "value", side_effect=[1, "test_user"])

    username = "test_user"

    result = user.read_user_username(username)

    assert result == {
        "user_id": 1,
        "username": "test_user",
    }
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()
    QSqlQuery.value.assert_any_call("user_id")
    QSqlQuery.value.assert_any_call("username")


def test_read_user_username_non_existing(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=False)

    username = "test_user"

    result = user.read_user_username(username)

    assert result is None
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()


def test_update_user(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)

    user_id = 1
    username = "updated_user"

    result = user.update_user(user_id, username)

    assert result is True
    QSqlQuery.exec.assert_called_once_with()


def test_delete_user(user, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)

    user_id = 1

    result = user.delete_user(user_id)

    assert result is True
    QSqlQuery.exec.assert_called_once_with()
