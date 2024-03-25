from unittest.mock import Mock
from controllers.seedController import SeedController


def test_check_input_valid():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    input = Mock(value=10)
    assert seed_controller.check_input(input) == True


def test_check_input_invalid():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    input = Mock(value=0)
    assert seed_controller.check_input(input) == False


def test_save_seed_gen_new_seed():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    seed_controller.seed_window = Mock(
        radio_gen_new_seed=Mock(isChecked=Mock(return_value=True)),
        seed_input=Mock(value=0),
        old_seed_continue=Mock(value=0),
        old_seed_regenerate=Mock(value=0),
    )
    seed_controller.pcgrng.get_random_number = Mock(return_value=12345)
    seed_controller.user_model.read_user_username = Mock(return_value={"user_id": 1})
    seed_controller.seed_model.create_seed = Mock()
    seed_controller.seed_window.close = Mock()

    seed_controller.save_seed()

    seed_controller.pcgrng.get_random_number.assert_called_once_with(1, 2**32 - 1)
    seed_controller.seed_model.create_seed.assert_called_once_with(12345, 1)
    seed_controller.seed_window.close.assert_called_once()


def test_save_seed_new_seed():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    seed_controller.seed_window = Mock(
        radio_gen_new_seed=Mock(isChecked=Mock(return_value=False)),
        radio_new_seed=Mock(isChecked=Mock(return_value=True)),
        seed_input=Mock(value=12345),
        old_seed_continue=Mock(value=0),
        old_seed_regenerate=Mock(value=0),
    )
    seed_controller.user_model.read_user_username = Mock(return_value={"user_id": 1})
    seed_controller.seed_model.create_seed = Mock()
    seed_controller.seed_window.close = Mock()

    seed_controller.save_seed()

    seed_controller.seed_model.create_seed.assert_called_once_with(12345, 1)
    seed_controller.seed_window.close.assert_called_once()


def test_save_seed_old_seed():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    seed_controller.seed_window = Mock(
        radio_gen_new_seed=Mock(isChecked=Mock(return_value=False)),
        radio_new_seed=Mock(isChecked=Mock(return_value=False)),
        radio_old_seed=Mock(isChecked=Mock(return_value=True)),
        old_seed_continue=Mock(value=12345),
        old_seed_regenerate=Mock(value=0),
    )
    seed_controller.user_model.read_user_username = Mock(return_value={"user_id": 1})
    seed_controller.seed_model.create_seed = Mock()
    seed_controller.seed_window.close = Mock()

    seed_controller.save_seed()

    seed_controller.seed_model.create_seed.assert_called_once_with(12345, 1)
    seed_controller.seed_window.close.assert_called_once()


def test_save_seed_continue_using_seed():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    seed_controller.seed_window = Mock(
        radio_gen_new_seed=Mock(isChecked=Mock(return_value=False)),
        radio_new_seed=Mock(isChecked=Mock(return_value=False)),
        radio_old_seed=Mock(isChecked=Mock(return_value=False)),
        radio_continue_using_seed=Mock(isChecked=Mock(return_value=True)),
        old_seed_continue=Mock(value=0),
        old_seed_regenerate=Mock(value=12345),
    )
    seed_controller.user_model.read_user_username = Mock(return_value={"user_id": 1})
    seed_controller.seed_model.create_seed = Mock()
    seed_controller.seed_window.close = Mock()

    seed_controller.save_seed()

    seed_controller.seed_model.create_seed.assert_called_once_with(12345, 1)
    seed_controller.seed_window.close.assert_called_once()


def test_save_seed_invalid_input():
    seed_controller = SeedController(Mock(), Mock(), Mock())
    seed_controller.seed_window = Mock(
        radio_gen_new_seed=Mock(isChecked=Mock(return_value=True)),
        seed_input=Mock(value=0),
        old_seed_continue=Mock(value=0),
        old_seed_regenerate=Mock(value=0),
    )
    seed_controller.pcgrng.get_random_number = Mock(return_value=12345)
    seed_controller.user_model.read_user_username = Mock(return_value={"user_id": 1})
    seed_controller.seed_model.create_seed = Mock()
    seed_controller.seed_window.close = Mock()

    seed_controller.save_seed()

    seed_controller.pcgrng.get_random_number.assert_not_called()
    seed_controller.seed_model.create_seed.assert_not_called()
    seed_controller.seed_window.close.assert_not_called()
