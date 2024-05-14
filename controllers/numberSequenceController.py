from PyQt6.QtWidgets import QPushButton, QLabel, QRadioButton, QSpinBox, QLineEdit
from typing import NamedTuple

from baseSequenceController import BaseSequenceController
from utils.PCGRNG import PCGRNG
from models.Seed import Seed
from models.User import User
from config import SESSION_NAME


class UIElements(NamedTuple):
    btn_generate_numbers: QPushButton
    btn_seed_numbers: QPushButton
    btn_clear_numbers: QPushButton
    sequence_name: QLineEdit
    l_bound: QSpinBox
    u_bound: QSpinBox
    label_lbound: QLabel
    label_ubound: QLabel
    n_groups: QSpinBox
    label_n_groups: QLabel
    n_elements: QSpinBox
    label_n_elements: QLabel
    original_order: QRadioButton
    ascending_order: QRadioButton
    descending_order: QRadioButton


class NumberSequenceController(BaseSequenceController):

    def __init__(
        self,
        ui_elements: UIElements,
        output_window,
    ) -> None:
        """
        Initializes the number sequence controller.
        """

        self.ui_elements = ui_elements
        self.output_window = output_window
        self.seed_model = Seed()
        self.user_model = User()
        self.pcgrng = PCGRNG()

        # Setup signals and slots for number sequence-related actions
        self.ui_elements.btn_clear_numbers.clicked.connect(self.clear_numbers)
        self.ui_elements.btn_generate_numbers.clicked.connect(self.print_sequence)

    def check_session(self):

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

    def clear_numbers(self):
        """
        Clears the input fields for number generation.
        """

        # Clear the input fields and reset placeholder values
        self.ui_elements.sequence_name.clear()
        self.ui_elements.sequence_name.setPlaceholderText("sequence 1")

        self.ui_elements.l_bound.clear()
        self.ui_elements.l_bound.setValue(0)

        self.ui_elements.u_bound.clear()
        self.ui_elements.u_bound.setValue(0)

        self.ui_elements.n_groups.clear()
        self.ui_elements.n_groups.setValue(1)

        self.ui_elements.n_elements.clear()
        self.ui_elements.n_elements.setValue(0)

        self.ui_elements.original_order.setChecked(True)
        self.ui_elements.ascending_order.setChecked(False)
        self.ui_elements.descending_order.setChecked(False)

        # Reset the stylesheets and tooltips for the input fields
        self.ui_elements.sequence_name.setStyleSheet("color: black; border: none;")
        self.ui_elements.l_bound.setStyleSheet("color: black; border: none;")
        self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")
        self.ui_elements.n_groups.setStyleSheet("color: black; border: none;")
        self.ui_elements.n_elements.setStyleSheet("color: black; border: none;")
        self.ui_elements.sequence_name.setToolTip("")
        self.ui_elements.l_bound.setToolTip("")
        self.ui_elements.u_bound.setToolTip("")
        self.ui_elements.n_groups.setToolTip("")
        self.ui_elements.n_elements.setToolTip("")

    def check_input_fields(self):
        """
        Checks if the input fields are valid.
        """

        # Check if the values are valid
        if self.ui_elements.sequence_name.text() == "":
            self.ui_elements.sequence_name.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.sequence_name.setToolTip("Sequence name cannot be empty")
            return
        else:
            self.ui_elements.sequence_name.setStyleSheet("color: black; border: none;")

        if self.ui_elements.l_bound.value() >= self.ui_elements.u_bound.value():
            self.ui_elements.l_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.l_bound.setToolTip(
                "Lower bound must be less than upper bound"
            )
            self.ui_elements.u_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.u_bound.setToolTip(
                "Upper bound must be greater than lower bound"
            )
            return
        else:
            self.ui_elements.l_bound.setStyleSheet("color: black; border: none;")
            self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")

        if self.ui_elements.l_bound.value() == 0:
            self.ui_elements.l_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.l_bound.setToolTip("Lower bound must be greater than 0")
            return
        else:
            self.ui_elements.l_bound.setStyleSheet("color: black; border: none;")
            self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")

        if self.ui_elements.u_bound.value() == 0:
            self.ui_elements.u_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.u_bound.setToolTip("Upper bound must be greater than 0")
            return
        else:
            self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")
            self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")

        if len(
            range(self.ui_elements.l_bound.value(), self.ui_elements.u_bound.value())
        ) < (self.ui_elements.n_elements.value() * self.ui_elements.n_groups.value()):
            self.ui_elements.n_elements.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_elements.setToolTip(
                "Number of elements must be less than the range of the lower and upper bounds"
            )
            return
        else:
            self.ui_elements.n_elements.setStyleSheet("color: black; border: none;")

        if self.ui_elements.n_groups.value() == 0:
            self.ui_elements.n_groups.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_groups.setToolTip(
                "Number of groups must be greater than 0"
            )
            return
        else:
            self.ui_elements.n_groups.setStyleSheet("color: black; border: none;")

        if self.ui_elements.n_elements.value() == 0:
            self.ui_elements.n_elements.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_elements.setToolTip(
                "Number of elements must be greater than 0"
            )
            return
        else:
            self.ui_elements.n_elements.setStyleSheet("color: black; border: none;")

    def generate_sequence(self):

        # Check if the input fields are valid
        self.check_input_fields()

        # Check if the user has an active session and set the seed
        self.check_session()

        # Generate the random numbers
        number_sequence = self.pcgrng.get_unique_random_number_sequence(
            self.ui_elements.l_bound.value(),
            self.ui_elements.u_bound.value(),
            (self.ui_elements.n_elements.value() * self.ui_elements.n_groups.value()),
        )

        return number_sequence

    def group_sequence(self, number_sequence):

        # Sort the date sequence based on the user's preference
        if self.ui_elements.ascending_order.isChecked():
            number_sequence = sorted(number_sequence)
        elif self.ui_elements.descending_order.isChecked():
            number_sequence = sorted(number_sequence, reverse=True)

        number_output = {}

        if self.ui_elements.n_groups.value() > 1:
            s = 0
            for i in range(self.ui_elements.n_groups.value()):

                number_output[f"group_{i + 1}"] = number_sequence[
                    s : s + self.ui_elements.n_elements.value()
                ]
                s += self.ui_elements.n_elements.value()

        else:
            number_output["group_1"] = number_sequence

        return number_output

    def print_sequence(self):

        # Generate the random numbers
        number_sequence = self.generate_sequence()

        # Group the numbers based on the user's preference
        number_output = self.group_sequence(number_sequence)

        # print the number_sequence
        self.output_window.output_element.clear()
        self.output_window.output_element.append(self.ui_elements.sequence_name)
        self.output_window.output_element.append("")

        for group, dates in number_output.items():
            self.output_window.output_element.append(group)
            for date in dates:
                self.output_window.output_element.append(date.strftime("%Y-%m-%d"))
            self.output_window.output_element.append("")
