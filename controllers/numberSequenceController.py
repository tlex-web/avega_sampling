from PyQt6.QtWidgets import QPushButton, QLabel, QRadioButton, QSpinBox, QLineEdit
from utils.PCGRNG import PCGRNG


class NumberSequenceController:

    def __init__(
        self,
        btn_generate_numbers: QPushButton,
        btn_seed_numbers: QPushButton,
        btn_clear_numbers: QPushButton,
        sequence_name: QLineEdit,
        l_bound: QSpinBox,
        u_bound: QSpinBox,
        label_lbound: QLabel,
        label_ubound: QLabel,
        n_groups: QSpinBox,
        label_n_groups: QLabel,
        n_elements: QSpinBox,
        label_n_elements: QLabel,
        original_order: QRadioButton,
        ascending_order: QRadioButton,
        descending_order: QRadioButton,
        output_window,
        seed_window,
    ) -> None:
        """
        Initializes the number sequence controller.
        """
        self.btn_generate_numbers = btn_generate_numbers
        self.btn_seed_numbers = btn_seed_numbers
        self.btn_clear_numbers = btn_clear_numbers
        self.sequence_name = sequence_name
        self.l_bound = l_bound
        self.u_bound = u_bound
        self.label_lbound = label_lbound
        self.label_ubound = label_ubound
        self.n_groups = n_groups
        self.label_n_groups = label_n_groups
        self.n_elements = n_elements
        self.label_n_elements = label_n_elements
        self.original_order = original_order
        self.ascending_order = ascending_order
        self.descending_order = descending_order
        self.output_window = output_window
        self.seed_window = seed_window

        # Setup signals and slots for number sequence-related actions
        self.btn_seed_numbers.clicked.connect(self.set_number_seed)
        self.btn_seed_numbers.clicked.connect(self.generate_seed)
        self.btn_clear_numbers.clicked.connect(self.clear_numbers)
        self.btn_generate_numbers.clicked.connect(self.generate_numbers)

    def set_number_seed(self):
        """
        Shows or hides the seed window for number generation based on its current visibility state.
        """
        if self.seed_window.isVisible():
            self.seed_window.close()
        else:
            self.seed_window.show()

    def generate_seed(self):
        """
        Generates a seed for the random number generator.
        """
        pass

    def set_seed(self):
        """
        Sets the seed for the random number generator.
        """
        self.seed_window.show()

        # determine the selected option and set the seed accordingly
        if self.seed_window.radio_gen_new_seed.isChecked():
            seed = self.seed_window.gen_new_seed.value()
        elif self.seed_window.radio_old_seed.isChecked():
            seed = self.seed_window.old_seed.value()
        elif self.seed_window.radio_con_old_seed.isChecked():
            seed = self.seed_window.con_old_seed.value()
        else:
            seed = None

        pcg = None

        if seed is not None:
            pcg = PCGRNG(initstate=seed)
        else:
            pcg = PCGRNG()

        return pcg

    def clear_numbers(self):
        """
        Clears the input fields for number generation.
        """
        self.sequence_name.clear()
        self.sequence_name.setPlaceholderText("sequence 1")

        self.l_bound.clear()
        self.l_bound.setValue(0)

        self.u_bound.clear()
        self.u_bound.setValue(0)

        self.n_groups.clear()
        self.n_groups.setValue(1)

        self.n_elements.clear()
        self.n_elements.setValue(0)

        self.original_order.setChecked(True)
        self.ascending_order.setChecked(False)
        self.descending_order.setChecked(False)

    def generate_numbers(self):
        """
        Generates random numbers based on the input fields and displays them in the output window.
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

        numbers = pcg.get_unique_random_sequence(l_bound, u_bound, n_elements)

        if n_groups > 1:
            numbers = sorted(numbers)
            numbers = [numbers[i::n_groups] for i in range(n_groups)]
        else:
            numbers = [numbers]

        if self.ascending_order.isChecked():
            numbers = [sorted(group) for group in numbers]
        elif self.descending_order.isChecked():
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
