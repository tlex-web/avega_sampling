import pytest
import os
from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
    QRadioButton,
    QSpinBox,
    QLineEdit,
    QDateEdit,
    QCheckBox,
    QGroupBox,
)
from PyQt6.QtGui import QAction
from unittest.mock import MagicMock, Mock, patch

from controllers.menuController import MenuController
from controllers.baseSequenceController import BaseSequenceController
from controllers.datesSequenceController import UIElementsDatesSequence
from controllers.projectController import ProjectController
from controllers.sessionController import SessionController
from controllers.windowController import WindowController
from db.Database import Database
from app import LoadingWindow, OutputWindow
from controllers.numberSequenceController import (
    NumberSequenceController,
    UIElementsNumberSequence,
)
from library.Logger import Logger
from library.PRNG.PCGRNG import PCGRNG
from library.helpers.PublicHolidays import PublicHolidays
from library.helpers.printOutput import PrintOutput
from models.Projects import Project
from models.RandomNumberSequenceGenerator import RandomNumberSequenceGenerator
from models.Seed import Seed
from models.User import User


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
    db.create_tables()
    yield db
    db.close()


@pytest.fixture
def ui_elements_number():
    return UIElementsNumberSequence(
        btn_generate_numbers=Mock(spec=QPushButton),
        btn_seed_numbers=Mock(spec=QPushButton),
        btn_clear_numbers=Mock(spec=QPushButton),
        sequence_name=Mock(spec=QLineEdit),
        l_bound=Mock(spec=QSpinBox),
        u_bound=Mock(spec=QSpinBox),
        label_lbound=Mock(spec=QLabel),
        label_ubound=Mock(spec=QLabel),
        n_groups=Mock(spec=QSpinBox),
        label_n_groups=Mock(spec=QLabel),
        n_elements=Mock(spec=QSpinBox),
        label_n_elements=Mock(spec=QLabel),
        original_order=Mock(spec=QRadioButton),
        ascending_order=Mock(spec=QRadioButton),
        descending_order=Mock(spec=QRadioButton),
    )


@pytest.fixture
def generator():
    return Mock(spec=NumberSequenceController)


@pytest.fixture
def loading_window():
    return Mock(spec=LoadingWindow)


@pytest.fixture
def output_window():
    return Mock(spec=OutputWindow)


@pytest.fixture
def public_holidays():
    return PublicHolidays()


@pytest.fixture
def mocker_ph():

    with patch("controllers.datesSequenceController.PublicHolidays") as mock:
        yield mock


@pytest.fixture
def ui_elements_dates():
    return UIElementsDatesSequence(
        btn_generate_dates=Mock(spec=QPushButton),
        btn_clear_dates=Mock(spec=QPushButton),
        exclude_bank_holidays=Mock(spec=QCheckBox),
        exclude_saturdays=Mock(spec=QCheckBox),
        exclude_sundays=Mock(spec=QCheckBox),
        sequence_name=Mock(spec=QLineEdit),
        l_bound=Mock(spec=QDateEdit),
        u_bound=Mock(spec=QDateEdit),
        label_lbound=Mock(spec=QLabel),
        label_ubound=Mock(spec=QLabel),
        exclude_dates=Mock(spec=QGroupBox),
        n_groups=Mock(spec=QSpinBox),
        label_n_groups=Mock(spec=QLabel),
        n_elements=Mock(spec=QSpinBox),
        label_n_elements=Mock(spec=QLabel),
        original_order=Mock(spec=QRadioButton),
        ascending_order=Mock(spec=QRadioButton),
        descending_order=Mock(spec=QRadioButton),
    )


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


@pytest.fixture
def project_controller(output_window):
    return ProjectController("Client", 2022, output_window)


@pytest.fixture
def hostname():
    return os.getenv("COMPUTERNAME")


@pytest.fixture
def session_controller():
    session_controller = SessionController()
    session_controller.model = MagicMock(User)
    return session_controller


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


@pytest.fixture
def print_output(output_window):
    company_name = "Sample Company"
    company_year = "2022"
    output = ["Output 1", "Output 2", "Output 3"]
    return PrintOutput(output_window, company_name, company_year, output)


@pytest.fixture
def logger():
    return Logger(isDev=True)


@pytest.fixture
def project():
    return Project()


@pytest.fixture
def rng_generator():
    generator = RandomNumberSequenceGenerator()
    generator.rng = MagicMock()
    return generator


@pytest.fixture
def seed():
    return Seed()


@pytest.fixture
def user():
    return User()


@pytest.fixture
def rng():
    return PCGRNG()
