import pytest

from fixtures import hostname, session_controller


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
