from PyQt6.QtWidgets import QPushButton, QLabel, QRadioButton, QSpinBox, QLineEdit
from typing import NamedTuple

from controllers.baseSequenceController import BaseSequenceController
from library.helpers.printOutput import PrintOutput, Output
from models.RandomNumberSequenceGenerator import RandomNumberSequenceGenerator
from library.custom_errors.InvalidInputError import InvalidInputError
from models.Seed import Seed
from models.User import User
from models.Projects import Project


class UIElementsNumberSequence(NamedTuple):
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
        ui_elements: UIElementsNumberSequence,
    ) -> None:
        """
        Initializes the number sequence controller.
        """
        super().__init__(RandomNumberSequenceGenerator())

        self.ui_elements = ui_elements
        self.print_output = PrintOutput()
        self.user_model = User()
        self.seed_model = Seed()
        self.project_model = Project()
        self.rng = RandomNumberSequenceGenerator()
        self.seed = None

        # Setup signals and slots for number sequence-related actions
        self.ui_elements.btn_clear_numbers.clicked.connect(self.clear_fields)
        # self.ui_elements.btn_seed_numbers.clicked.connect(self.set_seed)
        self.ui_elements.btn_generate_numbers.clicked.connect(
            self.handle_generate_sequence_btn
        )

    def clear_fields(self):
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
        self.ui_elements.sequence_name.setStyleSheet(
            "color: black; border: #fff 1px solid;"
        )
        self.ui_elements.l_bound.setStyleSheet("color: black; border: #fff 1px solid;")
        self.ui_elements.u_bound.setStyleSheet("color: black; border: #fff 1px solid;")
        self.ui_elements.n_groups.setStyleSheet("color: black; border: #fff 1px solid;")
        self.ui_elements.n_elements.setStyleSheet(
            "color: black; border: #fff 1px solid;"
        )
        self.ui_elements.sequence_name.setToolTip("")
        self.ui_elements.l_bound.setToolTip("")
        self.ui_elements.u_bound.setToolTip("")
        self.ui_elements.n_groups.setToolTip("")
        self.ui_elements.n_elements.setToolTip("")

    def reset_ui(self):
        """Reset UI elements to their default state."""

        self.ui_elements.sequence_name.setStyleSheet("")
        self.ui_elements.sequence_name.setToolTip("")

        self.ui_elements.l_bound.setStyleSheet("")
        self.ui_elements.l_bound.setToolTip("")

        self.ui_elements.u_bound.setStyleSheet("")
        self.ui_elements.u_bound.setToolTip("")

        self.ui_elements.n_groups.setStyleSheet("")
        self.ui_elements.n_groups.setToolTip("")

        self.ui_elements.n_elements.setStyleSheet("")
        self.ui_elements.n_elements.setToolTip("")

    def check_input_fields(self):
        """
        Checks if the input fields are valid.
        """

        # Check if the values are valid
        if self.ui_elements.sequence_name.text() == "":
            raise InvalidInputError("Sequence name cannot be empty")

        if self.ui_elements.l_bound.value() == 0:
            raise InvalidInputError("Lower bound must be greater than 0")

        if self.ui_elements.u_bound.value() == 0:
            raise InvalidInputError("Upper bound must be greater than 0")

        if self.ui_elements.l_bound.value() >= self.ui_elements.u_bound.value():
            raise InvalidInputError("Lower bound must be less than the upper bound")

        if self.ui_elements.n_groups.value() == 0:
            raise InvalidInputError("Number of groups must be greater than 0")

        if self.ui_elements.n_elements.value() == 0:
            raise InvalidInputError("Number of elements must be greater than 0")

        if len(
            range(self.ui_elements.l_bound.value(), self.ui_elements.u_bound.value())
        ) < (self.ui_elements.n_elements.value() * self.ui_elements.n_groups.value()):
            raise InvalidInputError(
                "The range of numbers must be greater than the number of elements"
            )

    def update_ui_for_errors(self, error):
        """Update UI elements to reflect input errors.

        Args:
            error (Exception): The error message
        """

        if "sequence name" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.sequence_name, str(error))
        if "lower bound" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.l_bound, str(error))
        if "upper bound" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.u_bound, str(error))
        if "number of groups" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.n_groups, str(error))
        if "number of elements" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.n_elements, str(error))
        if "range of numbers" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.l_bound, str(error))
            self.update_ui_for_invalid_input(self.ui_elements.u_bound, str(error))
        if "sequence generation" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.l_bound, str(error))

    def update_ui_for_invalid_input(self, field, message):
        """
        Updates the UI elements for invalid input.
        """

        field.setStyleSheet("color: red; border: 1px solid red;")
        field.setToolTip(message)

    def generate_sequence(self):

        # Reset the UI elements
        self.reset_ui()

        # Check if the input fields are valid
        self.check_input_fields()

        # Check if the user has an active session and set the seed
        if self.seed is None:
            self.ui_elements.btn_seed_numbers.click()

        # Generate the random numbers
        number_sequence = self.rng.generate_and_return_sequence(
            self.ui_elements.l_bound.value(),
            self.ui_elements.u_bound.value(),
            self.ui_elements.n_elements.value() * self.ui_elements.n_groups.value(),
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

    def set_seed(self):
        """
        Sets the seed for the random number generator.
        """

        # Get the user's session data
        session = self.read_session()

        # Set the seed for the random number generator
        if session is not None:
            self.seed = self.seed_model.read_seed(int(session["user_id"]))

            if self.seed is not None:
                self.rng.set_seed(int(self.seed["seed_value"]))
        else:
            self.seed = self.rng.set_seed()
            self.rng.set_seed(self.seed)

    def handle_generate_sequence_btn(self):

        try:
            self.set_seed()

            number_sequence = self.generate_sequence()

            number_output = self.group_sequence(number_sequence)

            self.print_output.set_output(
                Output(
                    lower_bound=self.ui_elements.l_bound.value(),
                    upper_bound=self.ui_elements.u_bound.value(),
                    optional_params={},
                    n_groups=self.ui_elements.n_groups.value(),
                    n_elements=self.ui_elements.n_elements.value(),
                    seed=self.rng.rng.state,
                    output=number_output,
                )
            )

            session = self.read_session()

            if session is not None:
                self.project_model.create_project(
                    self.ui_elements.sequence_name.text(),
                    int(session["user_id"]),
                    self.rng.rng.state,
                    self.ui_elements.l_bound.value(),
                    self.ui_elements.u_bound.value(),
                    self.ui_elements.n_elements.value(),
                    self.ui_elements.n_groups.value(),
                    str(number_output),
                )

        except InvalidInputError as e:
            self.update_ui_for_errors(e)
