import sys
from PyQt6 import QtWidgets, QtGui

from MainWindow import Ui_MainWindow
from OutputWindow import Ui_MainWindow as Ui_OutputWindow
from utils.PCGRNG import PCGRNG
from db.DB import Database

import resources  # needed for assets and correct packaging


class OutputWindow(QtWidgets.QMainWindow, Ui_OutputWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(OutputWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class SeedWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        # set title and icon
        self.setWindowTitle("Generate seed")
        self.setWindowIcon(QtGui.QIcon(":/icons/seed.png"))

        # create a radio button group to either generate a seed or enter a custom one
        self.radiobutton_group = QtWidgets.QButtonGroup()
        self.radiobutton_group.setExclusive(True)

        self.radiobutton_generate = QtWidgets.QRadioButton("Generate seed")
        self.radiobutton_generate.setChecked(True)
        self.radiobutton_generate.toggled.connect(self.generate_seed)

        self.radiobutton_custom = QtWidgets.QRadioButton("Enter custom seed")
        self.radiobutton_custom.toggled.connect(self.set_seed)

        self.radiobutton_group.addButton(self.radiobutton_generate)
        self.radiobutton_group.addButton(self.radiobutton_custom)

        layout.addWidget(self.radiobutton_generate)
        layout.addWidget(self.radiobutton_custom)

        # create a line edit to enter a custom seed
        self.lineedit_seed = QtWidgets.QLineEdit()
        self.lineedit_seed.setPlaceholderText("Enter seed")
        self.lineedit_seed.setEnabled(False)

        layout.addWidget(self.lineedit_seed)

        # create a button to generate a seed and close the window
        self.button_generate = QtWidgets.QPushButton("Generate")
        self.button_generate.clicked.connect(self.close_window)

        layout.addWidget(self.button_generate)

        self.setLayout(layout)

        # get the selected option from the radio button group after the window is closed and store it in a variable
        self.selected_option = self.radiobutton_group.checkedButton().text()

        # create a database object

    db = Database("db/pcg.db")

    def generate_seed(self):
        """Generates a seed for the random number generator"""

        # enable the line edit
        self.lineedit_seed.setEnabled(False)

        # generate a seed
        pcg = PCGRNG()
        seed = pcg.next()

        # check if the seed is in the database
        if self.db.query(f"SELECT * FROM seeds WHERE seed={seed}"):
            self.generate_seed()
        else:
            self.lineedit_seed.setText(str(seed))

        # add the seed to the database
        self.db.execute(f"INSERT INTO seeds VALUES ({seed})")

    def set_seed(self):
        """Sets the seed and closes the window"""

        # get the seed from the line edit
        seed = self.lineedit_seed.text()

        # check if the seed is valid
        if seed.isnumeric():
            seed = int(seed)
        else:
            self.lineedit_seed.setStyleSheet("color: red")
            return

        # check if the seed is in the database
        if self.db.query(f"SELECT * FROM seeds WHERE seed={seed}"):
            self.lineedit_seed.setStyleSheet("color: red")
            return
        else:
            self.lineedit_seed.setStyleSheet("color: black")

        # add the seed to the database
        self.db.execute(f"INSERT INTO seeds VALUES ({seed})")

    def close_window(self):
        """Closes the window"""
        self.close()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # setup the output window
        self.output_window = OutputWindow()

        self.pushButton_new_file.clicked.connect(self.new_file)
        self.pushButton_save_as.clicked.connect(self.save_as)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_copy.clicked.connect(self.copy)
        self.pushButton_paste.clicked.connect(self.paste)
        self.pushButton_help.clicked.connect(self.help)

        self.btn_generate_numbers.clicked.connect(self.generate_numbers)
        self.btn_seed_numbers.clicked.connect(self.generate_seed)

    def new_file(self):
        pass

    def save_as(self):
        pass

    def save(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def help(self):
        pass

    def generate_numbers(self):
        # get the values from the input fields and convert them to the correct type
        sequence_name = (
            self.sequence_name_numbers.text()
            if self.sequence_name_numbers.text() != ""
            else "sequence 1"
        )
        l_bound = int(self.lbound_numbers.text())
        u_bound = int(self.ubound_numbers.text())

        n_groups = int(self.n_groups_numbers.text())
        n_elements = int(self.n_elements_numbers.text())

        # check if the values are valid
        if l_bound >= u_bound:
            self.label_numbers_lbound.setStyleSheet("color: red")
            self.label_numbers_ubound.setStyleSheet("color: red")

            return
        else:
            self.label_numbers_lbound.setStyleSheet("color: black")
            self.label_numbers_ubound.setStyleSheet("color: black")

        if n_groups < 1:
            self.label_dates_n_groups.setStyleSheet("color: red")

            return
        else:
            self.label_dates_n_groups.setStyleSheet("color: black")

        if n_elements < 1:
            self.label_dates_n_elements.setStyleSheet("color: red")

            return
        else:
            self.label_dates_n_elements.setStyleSheet("color: black")

        pcg = PCGRNG(initstate=123)

        numbers = pcg.get_unique_random_sequence(l_bound, u_bound, n_elements)

        if n_groups > 1:
            numbers = sorted(numbers)
            numbers = [numbers[i::n_groups] for i in range(n_groups)]
        else:
            numbers = [numbers]

        if self.radiobutton_asc_numbers.isChecked():
            numbers = [sorted(group) for group in numbers]
        elif self.radiobutton_desc_numbers.isChecked():
            numbers = [sorted(group, reverse=True) for group in numbers]
        else:
            numbers = [group for group in numbers]

        if self.output_window.isVisible():
            self.output_window.close()
        else:
            self.output_window.show()

        # print the numbers
        self.output_window.output_element.clear()
        self.output_window.output_element.append(sequence_name)
        self.output_window.output_element.append("")
        for i, group in enumerate(numbers):
            self.output_window.output_element.append(f"Group {i+1}:")
            self.output_window.output_element.append(str(group))
            self.output_window.output_element.append("")

    def generate_seed(self):
        """Generates a seed for the random number generator"""
        pass


class App(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.window = MainWindow()
        self.window.show()


app = App(sys.argv)
sys.exit(app.exec())
