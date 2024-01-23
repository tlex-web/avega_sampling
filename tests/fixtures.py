import pytest
import os

from db.DB import Database


@pytest.fixture
def project_root():
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def app():
    from app import App

    return App()


@pytest.fixture
def window(app):
    return app.window


@pytest.fixture
def setup_database():
    db = Database(":memory:")
    db.connect()
    yield db
    db.close()
