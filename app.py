import sys
from PyQt6 import QtWidgets

from view.MainWindow import Ui_MainWindow
from view.OutputWindow import Ui_MainWindow as Ui_OutputWindow
from view.SeedWindow import Ui_Form as Ui_SeedWindow
from view.HelpWindow import Ui_MainWindow as Ui_HelpWindow
from view.LoadingWindow import Ui_Form as Ui_LoadingWindow

from controllers.userController import UserController
from controllers.projectController import ProjectController
from controllers.numberSequenceController import NumberSequenceController
from controllers.datesSequenceController import DatesSequenceController
from controllers.windowController import WindowController

from utils.PCGRNG import PCGRNG
from db.Database import Database
from config import DB_FILENAME

import resources  # needed for assets and correct packaging


# create global database object
db = Database(DB_FILENAME)


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

        # setup the controllers
        # self.user_controller = UserController(self)
        # self.project_controller = ProjectController(self)
        # self.number_sequence_controller = NumberSequenceController(self)
        # self.dates_sequence_controller = DatesSequenceController(self)

        # connect the signals and slots to handle events on the UI

        # Window signals
        self.window_controller = WindowController(
            self.pushButton_new_file,
            self.pushButton_save_as,
            self.pushButton_save,
            self.pushButton_copy,
            self.pushButton_paste,
            self.pushButton_help,
        )

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
