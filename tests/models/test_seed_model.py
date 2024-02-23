from PyQt6.QtSql import QSqlQuery

from models.Seed import Seed
from tests.fixtures import setup_database


def test_create_seed(setup_database):
    db = setup_database
    db.connect()

    seed = Seed()
    seed_value = "test_seed_create"
    project_id = 1

    assert seed.create_seed(seed_value, project_id)

    query = QSqlQuery()
    query.exec(
        f"SELECT * FROM seeds WHERE seed_value = '{seed_value}' AND project_id = {project_id}"
    )
    assert query.next()


def test_get_seed(setup_database):
    db = setup_database
    db.connect()

    seed = Seed()
    seed_value = "test_seed_get"
    project_id = 2

    query_insert = QSqlQuery()
    query_insert.prepare("INSERT INTO seeds (seed_value, project_id) VALUES (?, ?)")
    query_insert.addBindValue(seed_value)
    query_insert.addBindValue(project_id)
    query_insert.exec()

    seed_id = query_insert.lastInsertId()

    result = seed.get_seed(seed_id)
    assert result is not None
    assert result["seed_value"] == seed_value
    assert result["project_id"] == project_id


def test_get_seed_nonexistent(setup_database):
    db = setup_database
    db.connect()

    seed = Seed()
    seed_id = 9999

    result = seed.get_seed(seed_id)
    assert result is None
