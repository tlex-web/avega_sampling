from PyQt6.QtSql import QSqlQuery
from models.Projects import Project
from tests.fixtures import setup_database


def test_create_project(setup_database):
    db = setup_database
    db.connect()

    project = Project()
    project_name = "test_project_create"
    user_id = 1

    assert project.create_project(project_name, user_id)

    query = QSqlQuery()
    query.exec(
        f"SELECT * FROM projects WHERE project_name = '{project_name}' AND user_id = {user_id}"
    )
    assert query.next()


def test_update_project(setup_database):
    db = setup_database
    db.connect()

    project = Project()
    project_name = "test_project_update"
    user_id = 1
    new_project_name = "updated_project"
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO projects (project_name, user_id) VALUES (?, ?)")
    query_insert.addBindValue(project_name)
    query_insert.addBindValue(user_id)
    query_insert.exec()

    project_id = query_insert.lastInsertId()
    assert project.update_project(new_project_name, project_id, user_id)

    query = QSqlQuery()
    query.exec(f"SELECT * FROM projects WHERE project_id = {project_id}")
    assert query.next()
    assert query.value("project_name") == new_project_name


def test_delete_project(setup_database):
    db = setup_database
    db.connect()

    project = Project()
    project_name = "test_project_delete"
    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO projects (project_name) VALUES (?)")
    query_insert.addBindValue(project_name)
    query_insert.exec()

    project_id = query_insert.lastInsertId()
    assert project.delete_project(project_id)

    query = QSqlQuery()
    query.exec(f"SELECT * FROM projects WHERE project_id = {project_id}")
    assert not query.next()


def test_get_project(setup_database):
    db = setup_database
    db.connect()

    project = Project()
    project_id = 1

    result = project.get_project(project_id)
    assert result is not None
    assert result["project_id"] == project_id


def test_get_project_nonexistent(setup_database):
    db = setup_database
    db.connect()

    project = Project()
    project_id = 9999

    result = project.get_project(project_id)
    assert result is None
