import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QPushButton
from controllers.windowController import WindowController


@pytest.fixture
def window_controller():
    btn_new_file = MagicMock(spec=QPushButton)
    btn_save_as = MagicMock(spec=QPushButton)
    btn_save = MagicMock(spec=QPushButton)
    btn_copy = MagicMock(spec=QPushButton)
    btn_paste = MagicMock(spec=QPushButton)
    btn_help = MagicMock(spec=QPushButton)
    help_window = MagicMock()

    return WindowController(
        btn_new_file,
        btn_save_as,
        btn_save,
        btn_copy,
        btn_paste,
        btn_help,
        help_window,
    )


def test_new_file(window_controller):
    window_controller.new_file()
    # Add assertions here


def test_save_as(window_controller):
    window_controller.save_as()
    # Add assertions here


def test_save(window_controller):
    window_controller.save()
    # Add assertions here


def test_copy(window_controller):
    window_controller.copy()
    # Add assertions here


def test_paste(window_controller):
    window_controller.paste()
    # Add assertions here


def test_help_show(window_controller):
    window_controller.help_window.isVisible.return_value = False

    window_controller.help()

    window_controller.help_window.show.assert_called_once()


def test_help_hide(window_controller):
    window_controller.help_window.isVisible.return_value = True

    window_controller.help()

    window_controller.help_window.hide.assert_called_once()
