import pytest
from PyQt6.QtSql import QSqlQuery
from models.Seed import Seed


from fixtures import seed, mocker


def test_create_seed(seed, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)

    seed_value = 12345
    user_id = 1

    result = seed.create_seed(seed_value, user_id)

    assert result is True
    QSqlQuery.exec.assert_called_once_with()


def test_read_seed_existing(seed, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=True)
    mocker.patch.object(QSqlQuery, "value", side_effect=[12345, 1])

    user_id = 1

    result = seed.read_seed(user_id)

    assert result == {
        "seed_value": 12345,
        "user_id": 1,
    }
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()
    QSqlQuery.value.assert_any_call("seed_value")
    QSqlQuery.value.assert_any_call("user_id")


def test_read_seed_non_existing(seed, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=False)

    user_id = 1

    result = seed.read_seed(user_id)

    assert result is None
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()
