import pytest

from fixtures import base_sequence_controller, generator, mocker

from models.Seed import Seed
from models.User import User
from config import SESSION_NAME
from controllers.baseSequenceController import BaseSequenceController
from controllers.numberSequenceController import NumberSequenceController


def test_check_session_existing_user(base_sequence_controller, generator, mocker):
    mocker.patch.object(generator, "set_seed")

    generator.check_session()

    base_sequence_controller.read_user_username.assert_called_once_with(SESSION_NAME)
    base_sequence_controller.read_seed.assert_called_once_with(1)
    generator.set_seed.assert_called_once_with(12345)


def test_check_session_new_user(base_sequence_controller, mocker):
    mocker.patch.object(base_sequence_controller.generator, "set_seed")

    mocker.patch.object(User, "read_user_username", return_value=None)

    base_sequence_controller.check_session()

    User.read_user_username.assert_called_once_with(SESSION_NAME)
    Seed.read_seed.assert_not_called()
    base_sequence_controller.generator.set_seed.assert_called_once_with(None)


def test_clear_fields(base_sequence_controller):
    with pytest.raises(NotImplementedError):
        base_sequence_controller.clear_fields()


def test_check_input_fields(base_sequence_controller):
    with pytest.raises(NotImplementedError):
        base_sequence_controller.check_input_fields()


def test_generate_sequence(base_sequence_controller):
    with pytest.raises(NotImplementedError):
        base_sequence_controller.generate_sequence()


def test_handle_generate_sequence_btn(base_sequence_controller):
    with pytest.raises(NotImplementedError):
        base_sequence_controller.handle_generate_sequence_btn()
