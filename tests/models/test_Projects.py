import pytest_mock
from PyQt6.QtSql import QSqlQuery

from fixtures import project


mocker = pytest_mock.mocker


def test_create_project(project, mocker):
    mock_prepare = mocker.patch.object(QSqlQuery, "prepare")
    mock_exec = mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mock_bindValue = mocker.patch.object(QSqlQuery, "addBindValue")

    name = "Test Project"
    user_id = 1

    result = project.create_project(name, user_id)

    assert result is True
    mock_prepare.assert_called_once_with(
        "INSERT INTO projects (project_name, user_id) VALUES (?, ?)"
    )
    # Assert bindValue or similar methods as needed, depending on how parameters are bound
    # Example:
    mock_bindValue.assert_any_call(name)
    mock_bindValue.assert_any_call(user_id)
    mock_exec.assert_called_once()


def test_update_project(project, mocker):
    mock_prepare = mocker.patch.object(QSqlQuery, "prepare")
    mock_exec = mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mock_bindValue = mocker.patch.object(QSqlQuery, "addBindValue")

    name = "Test Project"
    project_id = 1
    user_id = 1

    result = project.update_project(name, project_id, user_id)

    assert result is True
    mock_prepare.assert_called_once_with(
        "UPDATE projects SET project_name = ? WHERE project_id = ? AND user_id = ?"
    )
    mock_bindValue.assert_any_call(name)
    mock_bindValue.assert_any_call(project_id)
    mock_bindValue.assert_any_call(user_id)
    mock_exec.assert_called_once()


def test_delete_project(project, mocker):
    mock_prepare = mocker.patch.object(QSqlQuery, "prepare")
    mock_exec = mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mock_bindValue = mocker.patch.object(QSqlQuery, "addBindValue")

    project_id = 1

    result = project.delete_project(project_id)

    assert result is True
    mock_prepare.assert_called_once_with("DELETE FROM projects WHERE project_id = ?")
    mock_bindValue.assert_any_call(project_id)
    mock_exec.assert_called_once()


def test_get_project_existing(project, mocker):
    mock_prepare = mocker.patch.object(QSqlQuery, "prepare")
    mock_exec = mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mock_next = mocker.patch.object(QSqlQuery, "next", return_value=True)
    mock_value = mocker.patch.object(
        QSqlQuery, "value", side_effect=[1, "Test Project", 1]
    )

    project_id = 1

    result = project.get_project(project_id)

    assert result == {
        "project_id": 1,
        "project_name": "Test Project",
        "user_id": 1,
    }
    mock_prepare.assert_called_once_with("SELECT * FROM projects WHERE project_id = ?")
    mock_next.assert_called_once()
    mock_exec.assert_called_once()
    mock_value.assert_any_call("project_id")
    mock_value.assert_any_call("project_name")


def test_get_project_non_existing(project, mocker):
    mock_prepare = mocker.patch.object(QSqlQuery, "prepare")
    mock_exec = mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mock_next = mocker.patch.object(QSqlQuery, "next", return_value=False)

    project_id = 1

    result = project.get_project(project_id)

    assert result is None
    mock_prepare.assert_called_once_with("SELECT * FROM projects WHERE project_id = ?")
    mock_next.assert_called_once()
    mock_exec.assert_called_once()
