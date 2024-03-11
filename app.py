import sys
import traceback
from PyQt6 import QtWidgets

from view.MainWindow import Ui_MainWindow
from view.OutputWindow import Ui_MainWindow as Ui_OutputWindow
from view.SeedWindow import Ui_Form as Ui_SeedWindow
from view.HelpWindow import Ui_MainWindow as Ui_HelpWindow
from view.LoadingWindow import Ui_Form as Ui_LoadingWindow
from view.AboutWindow import Ui_Form as Ui_AboutWindow

from controllers.seedController import SeedController
from controllers.userController import UserController
from controllers.projectController import ProjectController
from controllers.numberSequenceController import NumberSequenceController
from controllers.datesSequenceController import DatesSequenceController
from controllers.windowController import WindowController
from controllers.menuController import MenuController

from utils.Logger import Logger, LogEnvironment

from utils.PCGRNG import PCGRNG
from db.Database import Database
from config import DB_FILENAME, IS_DEV

import resources  # needed for assets and correct packaging


# create global database object
db = Database(DB_FILENAME)

log = Logger(IS_DEV)


class OutputWindow(QtWidgets.QMainWindow, Ui_OutputWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(OutputWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class SeedWindow(QtWidgets.QWidget, Ui_SeedWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(SeedWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class HelpWindow(QtWidgets.QWidget, Ui_HelpWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(HelpWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class LoadingWindow(QtWidgets.QWidget, Ui_LoadingWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(LoadingWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class AboutWindow(QtWidgets.QWidget, Ui_AboutWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(AboutWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    Inherits from QtWidgets.QMainWindow and Ui_MainWindow.
    """

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # setup the output window
        self.output_window = OutputWindow()

        # setup the seed window
        self.seed_window = SeedWindow()

        # setup the loading window
        self.loading_window = LoadingWindow()

        # setup the help window
        self.help_window = HelpWindow()

        # setup the about window
        self.about_window = AboutWindow()

        # connect the signals and slots to handle events on the UI

        # Window signals
        self.window_controller = WindowController(
            self.pushButton_new_file,
            self.pushButton_save_as,
            self.pushButton_save,
            self.pushButton_copy,
            self.pushButton_paste,
            self.pushButton_help,
            self.help_window,
        )

        # Menu signals
        self.menu_controller = MenuController(
            self.actionSave,
            self.actionSave_as,
            self.actionAbout,
            self.actionHow_to,
            self.about_window,
            self.help_window,
        )

        # User tab signals
        # self.user_controller = UserController(self)

        # Project tab signals
        # self.project_controller = ProjectController(self)

        # Number Sequence tab signals
        self.number_sequence_controller = NumberSequenceController(
            self.btn_generate_numbers,
            self.btn_seed_numbers,
            self.btn_clear_numbers,
            self.sequence_name_numbers,
            self.lbound_numbers,
            self.ubound_numbers,
            self.label_numbers_lbound,
            self.label_dates_ubound,
            self.n_groups_numbers,
            self.label_numbers_n_groups,
            self.n_elements_numbers,
            self.label_numbers_n_elements,
            self.radiobutton_org_numbers,
            self.radiobutton_asc_numbers,
            self.radiobutton_desc_numbers,
            self.output_window,
            self.seed_window,
        )

        # Dates Sequence tab signals
        # self.dates_sequence_controller = DatesSequenceController(
        #     self.btn_generate_dates,
        #     self.btn_seed_dates,
        #     self.btn_clear_dates,
        #     self.sequence_name_dates,
        #     self.lbound_dates,
        #     self.ubound_dates,
        #     self.label_dates_lbound,
        #     self.label_dates_ubound,
        #     self.exclude_dates,
        #     self.n_groups_dates,
        #     self.label_dates_n_groups,
        #     self.n_elements_dates,
        #     self.label_dates_n_elements,
        #     self.radiobutton_org_dates,
        #     self.radiobutton_asc_dates,
        #     self.radiobutton_desc_dates,
        #     self.output_window,
        #     self.seed_window,
        # )

        # Seed Window signals
        self.seed_controller = SeedController(self.seed_window)


# Monetary Unit Sampling tab signals and slots
#############################
# To be implemented later
#############################


class App(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":

    app = App(sys.argv)
    sys.exit(app.exec())
