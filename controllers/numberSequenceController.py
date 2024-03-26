from PyQt6.QtWidgets import QPushButton, QLabel, QRadioButton, QSpinBox, QLineEdit
from PyQt6.QtCore import Qt
from utils.PCGRNG import PCGRNG
from models.Seed import Seed
from models.User import User
from config import SESSION_NAME


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
        self.seed_model = Seed()
        self.user_model = User()
        self.pcgrng = PCGRNG()

        # Setup signals and slots for number sequence-related actions
        self.btn_clear_numbers.clicked.connect(self.clear_numbers)
        self.btn_generate_numbers.clicked.connect(self.generate_numbers)

    def clear_numbers(self):
        """
        Clears the input fields for number generation.
        """

        # Clear the input fields and reset placeholder values
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

        # Reset the stylesheets and tooltips for the input fields
        self.sequence_name.setStyleSheet("color: black; border: none;")
        self.l_bound.setStyleSheet("color: black; border: none;")
        self.u_bound.setStyleSheet("color: black; border: none;")
        self.n_groups.setStyleSheet("color: black; border: none;")
        self.n_elements.setStyleSheet("color: black; border: none;")
        self.sequence_name.setToolTip("")
        self.l_bound.setToolTip("")
        self.u_bound.setToolTip("")
        self.n_groups.setToolTip("")
        self.n_elements.setToolTip("")

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

        # Initialize a flag for valid values
        valid_values = True

        # Check if the values are valid
        if l_bound >= u_bound:
            self.l_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.l_bound.setToolTip("Lower bound must be greater than lower bound")
            self.u_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.u_bound.setToolTip("Upper bound must be greater than lower bound")
            valid_values = False
        else:
            self.l_bound.setStyleSheet("color: black; border: none;")
            self.u_bound.setStyleSheet("color: black; border: none;")

        if n_groups < 1:
            self.n_groups.setStyleSheet("color: red; border: 1px solid red;")
            self.n_groups.setToolTip("Number of groups must be greater than 0")
            valid_values = False
        else:
            self.n_groups.setStyleSheet("color: black; border: none;")

        if n_elements < 1:
            self.n_elements.setStyleSheet("color: red; border: 1px solid red;")
            self.n_elements.setToolTip("Number of elements must be greater than 0")
            valid_values = False
        else:
            self.n_elements.setStyleSheet("color: black; border: none;")

        # If any of the values are invalid, return
        if not valid_values:
            return

        # Set the seed for the random number generator

        # 1) Check if the user has set a seed
        # 2) If not, generate a seed
        # 3) If yes, use the user's seed
        # 4) Set the seed for the random number generator
        user_dict = self.user_model.read_user_username(SESSION_NAME)

        if user_dict is not None:
            user_id = user_dict["user_id"]

        seed = self.seed_model.read_seed(user_id)

        if seed is not None:
            seed_value = seed["seed_value"]
        else:
            seed_value = self.pcgrng.get_random_number(1, 2**32 - 1)

        self.pcgrng.seed(seed_value)

        numbers = self.pcgrng.get_unique_random_number_sequence(
            l_bound, u_bound, n_elements
        )

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
