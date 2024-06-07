import pytest
from PyQt6.QtSql import QSqlQuery
from models.Projects import Project


@pytest.fixture
def project():
    return Project()


def test_create_project(project, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)

    name = "Test Project"
    user_id = 1

    result = project.create_project(name, user_id)

    assert result is True
    QSqlQuery.exec.assert_called_once_with()


def test_update_project(project, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)

    name = "Updated Project"
    project_id = 1
    user_id = 1

    result = project.update_project(name, project_id, user_id)

    assert result is True
    QSqlQuery.exec.assert_called_once_with()


def test_delete_project(project, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)

    project_id = 1

    result = project.delete_project(project_id)

    assert result is True
    QSqlQuery.exec.assert_called_once_with()


def test_get_project_existing(project, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=True)
    mocker.patch.object(QSqlQuery, "value", side_effect=["1", "Test Project", "1"])

    project_id = 1

    result = project.get_project(project_id)

    assert result == {
        "project_id": "1",
        "project_name": "Test Project",
        "user_id": "1",
    }
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()
    QSqlQuery.value.assert_any_call("project_id")
    QSqlQuery.value.assert_any_call("project_name")
    QSqlQuery.value.assert_any_call("user_id")


def test_get_project_non_existing(project, mocker):
    mocker.patch.object(QSqlQuery, "exec", return_value=True)
    mocker.patch.object(QSqlQuery, "next", return_value=False)

    project_id = 1

    result = project.get_project(project_id)

    assert result is None
    QSqlQuery.exec.assert_called_once_with()
    QSqlQuery.next.assert_called_once_with()
