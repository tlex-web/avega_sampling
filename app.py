import sys
from PyQt6 import QtWidgets

from MainWindow import Ui_MainWindow
from OutputWindow import Ui_MainWindow as Ui_OutputWindow
from SeedWindow import Ui_Form as Ui_SeedWindow
from utils.PCGRNG import PCGRNG
from db.DB import Database

import resources  # needed for assets and correct packaging


# create global database object
db = Database("seed_store.db")


class OutputWindow(QtWidgets.QMainWindow, Ui_OutputWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(OutputWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


class SeedWindow(QtWidgets.QWidget, Ui_SeedWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(SeedWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)


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

    def set_seed(self):
        """Sets the seed for the random number generator"""

        seed_window = SeedWindow()
        seed_window.show()

        # determine the selected option and set the seed accordingly
        if seed_window.radio_gen_new_seed.isChecked():
            seed = seed_window.gen_new_seed.value()
        elif seed_window.radio_old_seed.isChecked():
            seed = seed_window.old_seed.value()
        elif seed_window.radio_con_old_seed.isChecked():
            seed = seed_window.con_old_seed.value()
        else:
            seed = None

        pcg = None

        if seed is not None:
            pcg = PCGRNG(initstate=seed)
        else:
            pcg = PCGRNG()

        return pcg


class App(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.window = MainWindow()
        self.window.show()


app = App(sys.argv)
sys.exit(app.exec())
