import pytest
import os

from db.Database import Database
from utils.FetchPublicHolidays import FetchPublicHolidays
from utils.PCGRNG import PCGRNG


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
    db = Database("./tests/test.db")
    yield db

    db.close()
    os.remove("./tests/test.db")
