import sys
from PyQt6 import QtWidgets


from view.MainWindow import Ui_MainWindow
from view.OutputWindow import Ui_MainWindow as Ui_OutputWindow
from view.SeedWindow import Ui_Form as Ui_SeedWindow
from view.HelpWindow import Ui_MainWindow as Ui_HelpWindow
from view.LoadingWindow import Ui_Form as Ui_LoadingWindow
from view.AboutWindow import Ui_Form as Ui_AboutWindow

from controllers.seedController import SeedController
from controllers.sessionController import SessionController
from controllers.outputController import OutputWindowController
from controllers.numberSequenceController import NumberSequenceController
from controllers.datesSequenceController import DatesSequenceController
from controllers.windowController import WindowController
from controllers.menuController import MenuController
from controllers.numberSequenceController import UIElementsNumberSequence
from controllers.datesSequenceController import UIElementsDatesSequence

from library.helpers.printOutput import PrintOutput
from library.EventManager import EventManager

from db.Database import Database
from config import DB_FILENAME

import resources  # ignore: needed for assets and correct packaging

# create database object
db = Database(DB_FILENAME)
db.connect()
db.create_tables()

# create user session and exit if no session is found
try:
    session_controller = SessionController()
    session_controller.init_session()
except Exception as e:
    exit(1)


class OutputWindow(QtWidgets.QMainWindow, Ui_OutputWindow):
    def __init__(self, *args, **kwargs):
        super(OutputWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class SeedWindow(QtWidgets.QWidget, Ui_SeedWindow):
    def __init__(self, *args, **kwargs):
        super(SeedWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class HelpWindow(QtWidgets.QWidget, Ui_HelpWindow):
    def __init__(self, *args, **kwargs):
        super(HelpWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class LoadingWindow(QtWidgets.QWidget, Ui_LoadingWindow):
    def __init__(self, *args, **kwargs):
        super(LoadingWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class AboutWindow(QtWidgets.QWidget, Ui_AboutWindow):
    def __init__(self, *args, **kwargs):
        super(AboutWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    Inherits from QtWidgets.QMainWindow and Ui_MainWindow.
    """

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # setup the event manager
        event_manager = EventManager()

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
        self.signals = PrintOutput()

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

        # Output Window signals
        self.output_controller = OutputWindowController(
            self.output_window,
            event_manager,
            self.btn_generate_numbers,
            self.btn_generate_dates,
        )

        # Connect request_seed signal to show the seed window
        event_manager.request_seed.connect(self.seed_window.show)

        # Number Sequence tab signals
        self.number_sequence_controller = NumberSequenceController(
            ui_elements=UIElementsNumberSequence(
                btn_generate_numbers=self.btn_generate_numbers,
                btn_seed_numbers=self.btn_seed_numbers,
                btn_clear_numbers=self.btn_clear_numbers,
                sequence_name=self.sequence_name_numbers,
                l_bound=self.lbound_numbers,
                u_bound=self.ubound_numbers,
                label_lbound=self.label_numbers_lbound,
                label_ubound=self.label_numbers_ubound,
                n_groups=self.n_groups_numbers,
                label_n_groups=self.label_numbers_n_groups,
                n_elements=self.n_elements_numbers,
                label_n_elements=self.label_numbers_n_elements,
                original_order=self.radiobutton_org_numbers,
                ascending_order=self.radiobutton_asc_numbers,
                descending_order=self.radiobutton_desc_numbers,
            ),
            event_manager=event_manager,
        )

        # Dates Sequence tab signals
        self.dates_sequence_controller = DatesSequenceController(
            ui_elements=UIElementsDatesSequence(
                btn_generate_dates=self.btn_generate_dates,
                btn_clear_dates=self.btn_clear_dates,
                btn_seed_dates=self.btn_seed_dates,
                exclude_bank_holidays=self.exclude_bank_holidays,
                exclude_saturdays=self.exclude_saturdays,
                exclude_sundays=self.exclude_sundays,
                sequence_name=self.sequence_name_dates,
                l_bound=self.lbound_dates,
                u_bound=self.ubound_dates,
                label_lbound=self.label_dates_lbound,
                label_ubound=self.label_dates_ubound,
                exclude_dates=self.exclude_dates,
                n_groups=self.n_groups_dates,
                label_n_groups=self.label_dates_n_groups,
                n_elements=self.n_elements_dates,
                label_n_elements=self.label_dates_n_elements,
                original_order=self.radiobutton_org_dates,
                ascending_order=self.radiobutton_asc_dates,
                descending_order=self.radiobutton_desc_dates,
            ),
            output_window=self.output_window,
            loading_window=self.loading_window,
        )

        # Seed Window signals
        self.seed_controller = SeedController(
            self.seed_window, event_manager, self.btn_seed_numbers, self.btn_seed_dates
        )


# Monetary Unit Sampling tab signals and slots
#############################
# To be implemented later
#############################


class App(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        # create the main window
        self.window = MainWindow()
        self.window.show()


import logging

if __name__ == "__main__":

    app = App(sys.argv)
    logging.basicConfig()
    sys.exit(app.exec())
