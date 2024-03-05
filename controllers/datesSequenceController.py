from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
    QRadioButton,
    QSpinBox,
    QLineEdit,
    QGroupBox,
)
from app import OutputWindow, SeedWindow
from utils.PCGRNG import PCGRNG


class DatesSequenceController:

    def __init__(
        self,
        btn_generate_dates: QPushButton,
        btn_seed_dates: QPushButton,
        btn_clear_dates: QPushButton,
        sequence_name: QLineEdit,
        l_bound: QSpinBox,
        u_bound: QSpinBox,
        label_lbound: QLabel,
        label_ubound: QLabel,
        exclude_dates: QGroupBox,
        n_groups: QSpinBox,
        label_n_groups: QLabel,
        n_elements: QSpinBox,
        label_n_elements: QLabel,
        ascending_order: QRadioButton,
        descending_order: QRadioButton,
        output_window: OutputWindow,
        seed_window: SeedWindow,
    ) -> None:
        """
        Initializes the number sequence controller.
        """
        self.btn_generate_dates = btn_generate_dates
        self.btn_seed_dates = btn_seed_dates
        self.btn_clear_dates = btn_clear_dates
        self.sequence_name = sequence_name
        self.l_bound = l_bound
        self.u_bound = u_bound
        self.label_lbound = label_lbound
        self.label_ubound = label_ubound
        self.exclude_dates = exclude_dates
        self.n_groups = n_groups
        self.label_n_groups = label_n_groups
        self.n_elements = n_elements
        self.label_n_elements = label_n_elements
        self.ascending_order = ascending_order
        self.descending_order = descending_order
        self.output_window = output_window
        self.seed_window = seed_window

        # Setup signals and slots for number sequence-related actions
        self.btn_seed_dates.clicked.connect(self.set_dates_seed)
        self.btn_generate_dates.clicked.connect(self.generate_dates)
        self.btn_seed_dates.clicked.connect(self.generate_seed)
        self.btn_clear_dates.clicked.connect(self.clear_dates)
        self.btn_generate_dates.clicked.connect(self.generate_dates)

    def set_dates_seed(self):
        """
        Shows or hides the seed window for date generation based on its current visibility state.
        """
        if self.seed_window.isVisible():
            self.seed_window.close()
        else:
            self.seed_window.show()

    def generate_seed(self):
        """
        Generates a seed for the date generation and displays it in the output window.
        """
        pcg = PCGRNG(initstate=123)

        seed = pcg.get_random_number(1, 10000)

        if self.output_window.isVisible():
            self.output_window.close()
        else:
            self.output_window.show()

        self.output_window.output_element.clear()
        self.output_window.output_element.append(f"Seed: {seed}")

    def clear_dates(self):
        """
        Clears the input fields for date generation.
        """
        self.sequence_name.clear()
        self.l_bound.clear()
        self.u_bound.clear()
        self.exclude_dates.clearMask()
        self.n_groups.clear()
        self.n_elements.clear()
        self.ascending_order.setChecked(True)
        self.descending_order.setChecked(False)

    def generate_dates(self):
        """
        Generates random dates based on the input fields and displays them in the output window.
        """
        # get the values from the input fields and convert them to the correct type
        sequence_name = (
            self.sequence_name.text()
            if self.sequence_name.text() != ""
            else "sequence 1"
        )
        l_bound = int(self.l_bound.text())
        u_bound = int(self.u_bound.text())

        n_groups = int(self.n_groups.text())
        n_elements = int(self.n_elements.text())

        # check if the values are valid
        if l_bound >= u_bound:
            self.label_lbound.setStyleSheet("color: red")
            self.label_ubound.setStyleSheet("color: red")

            return
        else:
            self.label_lbound.setStyleSheet("color: black")
            self.label_ubound.setStyleSheet("color: black")

        if n_groups < 1:
            self.label_n_groups.setStyleSheet("color: red")

            return
        else:
            self.label_n_groups.setStyleSheet("color: black")

        if n_elements < 1:
            self.label_n_elements.setStyleSheet("color: red")

            return
        else:
            self.label_n_elements.setStyleSheet("color: black")

        pcg = PCGRNG(initstate=123)

        dates = pcg.get_unique_random_sequence(l_bound, u_bound, n_elements)

        if n_groups > 1:
            dates = sorted(dates)
            dates = [dates[i::n_groups] for i in range(n_groups)]
        else:
            dates = [dates]

        if self.ascending_order.isChecked():
            dates = [sorted(group) for group in dates]
        elif self.descending_order.isChecked():
            dates = [sorted(group, reverse=True) for group in dates]
        else:
            dates = [group for group in dates]

        if self.output_window.isVisible():
            self.output_window.close()
        else:
            self.output_window.show()

        # print the dates
        self.output_window.output_element.clear()
        self.output_window.output_element.append(sequence_name)
        self.output_window.output_element.append("")
        for i, group in enumerate(dates):
            self.output_window.output_element.append(f"Group {i+1}:")
            self.output_window.output_element.append(str(group))
            self.output_window.output_element.append("")
