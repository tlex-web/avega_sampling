import os
import pytest
from unittest.mock import MagicMock
from controllers.sessionController import SessionController
from models.User import User
from library.Logger import Logger, LogEnvironment

# save the local machine name
hostname = os.getenv("COMPUTERNAME")


@pytest.fixture
def session_controller():
    session_controller = SessionController()
    session_controller.model = MagicMock(User)
    return session_controller


def test_init_session_new_session(session_controller):
    session_controller.model.read_user_username.return_value = None
    session_controller.model.create_user.return_value = 12345

    session_controller.init_session()

    session_controller.model.read_user_username.assert_called_once_with(hostname)
    session_controller.model.create_user.assert_called_once_with(hostname)


def test_init_session_existing_session(session_controller):
    session_controller.model.read_user_username.return_value = {"user_id": 54321}

    session_controller.init_session()

    session_controller.model.read_user_username.assert_called_once_with(hostname)


def test_init_session_failed_to_start_session(session_controller):
    session_controller.model.read_user_username.return_value = None
    session_controller.model.create_user.return_value = None

    with pytest.raises(Exception):
        session_controller.init_session()

    session_controller.model.read_user_username.assert_called_once_with(hostname)
    session_controller.model.create_user.assert_called_once_with(hostname)
