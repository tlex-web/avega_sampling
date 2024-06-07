import pytest
from PyQt6.QtGui import QAction
from unittest.mock import MagicMock

from controllers.menuController import MenuController


@pytest.fixture
def menu_controller(qtbot):
    btn_action_save = QAction()
    btn_action_save_as = QAction()
    btn_action_about = QAction()
    btn_action_how_to = QAction()
    about_window = MagicMock()
    help_window = MagicMock()

    controller = MenuController(
        btn_action_save,
        btn_action_save_as,
        btn_action_about,
        btn_action_how_to,
        about_window,
        help_window,
    )

    qtbot.addWidget(controller.about_window)
    qtbot.addWidget(controller.help_window)

    return controller


def test_save(menu_controller, capsys):
    menu_controller.save()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Save"


def test_save_as(menu_controller, capsys):
    menu_controller.save_as()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Save as"


def test_about(menu_controller):
    menu_controller.about()
    menu_controller.about_window.show.assert_called_once()


def test_how_to(menu_controller):
    menu_controller.how_to()
    menu_controller.help_window.show.assert_called_once()
