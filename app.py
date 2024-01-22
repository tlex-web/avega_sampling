import sys
from unittest.util import sorted_list_difference
from PyQt6 import QtWidgets
from PyQt6.QtGui import QMouseEvent

from MainWindow import Ui_MainWindow
from PCGRNG import PCGRNG


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.pushButton_new_file.clicked.connect(self.new_file)
        self.pushButton_save_as.clicked.connect(self.save_as)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_copy.clicked.connect(self.copy)
        self.pushButton_paste.clicked.connect(self.paste)
        self.pushButton_help.clicked.connect(self.help)

        self.btn_generate_numbers.clicked.connect(self.generate_numbers)

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
        print("generate_numbers")

        # get the values from the input fields
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

        # print the numbers
        self.output_element.clear()
        self.output_element.append(sequence_name)
        for i in range(n_groups):
            self.output_element.append(f"Group {i + 1}: {numbers[i]}")
        self.output_element.append("")


class App(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.window = MainWindow()
        self.window.show()


app = App(sys.argv)
sys.exit(app.exec())
