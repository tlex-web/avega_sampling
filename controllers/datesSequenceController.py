from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
    QRadioButton,
    QCheckBox,
    QSpinBox,
    QLineEdit,
    QGroupBox,
    QDateEdit,
)
from PyQt6.QtCore import QPropertyAnimation
from datetime import date, timedelta
from typing import NamedTuple

from controllers.baseSequenceController import BaseSequenceController

from models.RandomDatesSequenceGenerator import RandomDatesSequenceGenerator
from library.helpers.PublicHolidays import PublicHolidays
from library.custom_errors.InvalidInputError import InvalidInputError

from models.Seed import Seed
from models.User import User


class UIElementsDatesSequence(NamedTuple):
    btn_generate_dates: QPushButton
    btn_clear_dates: QPushButton
    btn_seed_dates: QPushButton
    exclude_bank_holidays: QCheckBox
    exclude_saturdays: QCheckBox
    exclude_sundays: QCheckBox
    sequence_name: QLineEdit
    l_bound: QDateEdit
    u_bound: QDateEdit
    label_lbound: QLabel
    label_ubound: QLabel
    exclude_dates: QGroupBox
    n_groups: QSpinBox
    label_n_groups: QLabel
    n_elements: QSpinBox
    label_n_elements: QLabel
    original_order: QRadioButton
    ascending_order: QRadioButton
    descending_order: QRadioButton


class DatesSequenceController(BaseSequenceController):

    def __init__(
        self,
        ui_elements: UIElementsDatesSequence,
        output_window,
        loading_window,
    ) -> None:
        """
        Initializes the number sequence controller.
        """
        super().__init__(RandomDatesSequenceGenerator())

        self.ui_elements = ui_elements
        self.output_window = output_window
        self.loading_window = loading_window
        self.seed_model = Seed()
        self.user_model = User()
        self.public_holidays = PublicHolidays()
        self.rdg = RandomDatesSequenceGenerator()
        self.list_public_holidays = None
        self.seed = None

        # Setup signals and slots for number sequence-related actions
        self.ui_elements.btn_clear_dates.clicked.connect(self.clear_fields)
        self.ui_elements.btn_generate_dates.clicked.connect(self.generate_emit_sequence)

    def clear_fields(self):
        """
        Clear the input fields for date generation and reset placeholder values.
        """

        # Clear the input fields and reset placeholder values
        self.ui_elements.sequence_name.clear()
        self.ui_elements.sequence_name.setPlaceholderText("Enter sequence name")

        self.ui_elements.l_bound.clear()
        self.ui_elements.l_bound.setDate(self.ui_elements.l_bound.minimumDate())

        self.ui_elements.u_bound.clear()
        self.ui_elements.u_bound.setDate(self.ui_elements.u_bound.maximumDate())

        self.ui_elements.exclude_dates.clearMask()

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

    def reset_ui(self):
        """Reset UI elements to their default state."""

        self.ui_elements.sequence_name.setStyleSheet("color: black; border: none;")
        self.ui_elements.sequence_name.setToolTip("")

        self.ui_elements.l_bound.setStyleSheet("color: black; border: none;")
        self.ui_elements.l_bound.setToolTip("")

        self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")
        self.ui_elements.u_bound.setToolTip("")

        self.ui_elements.n_groups.setStyleSheet("color: black; border: none;")
        self.ui_elements.n_groups.setToolTip("")

        self.ui_elements.n_elements.setStyleSheet("color: black; border: none;")
        self.ui_elements.n_elements.setToolTip("")

    def check_input_fields(self):
        # Check if the values are valid
        if self.ui_elements.sequence_name.text() == "":
            raise InvalidInputError("Sequence name cannot be empty")
        if (
            self.ui_elements.l_bound.date().toPyDate()
            >= self.ui_elements.u_bound.date().toPyDate()
        ):
            raise InvalidInputError("Lower bound must be less than upper bound")

        if self.ui_elements.n_groups.value() < 1:
            raise InvalidInputError("Number of groups must be greater than 0")

        if self.ui_elements.n_elements.value() < 1:
            raise InvalidInputError("Number of elements must be greater than 0")

        if len(
            [
                self.ui_elements.l_bound.date().toPyDate() + timedelta(days=x)
                for x in range(
                    (
                        self.ui_elements.u_bound.date().toPyDate()
                        - self.ui_elements.l_bound.date().toPyDate()
                    ).days
                    + 1
                )
            ]
        ) < (self.ui_elements.n_elements.value() * self.ui_elements.n_groups.value()):
            raise InvalidInputError(
                "Extend the period or reduce the number of elements or groups"
            )

    def update_ui_for_errors(self, error):
        """Update UI elements to reflect input errors.

        Args:
            error (Exception): The error message
        """

        if "sequence name" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.sequence_name, str(error))
        if "lower bound must be less than upper bound" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.l_bound, str(error))
            self.update_ui_for_invalid_input(self.ui_elements.u_bound, str(error))
        if "number of groups" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.n_groups, str(error))
        if "number of elements" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.n_elements, str(error))
        if "range of numbers" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.l_bound, str(error))
            self.update_ui_for_invalid_input(self.ui_elements.u_bound, str(error))
        if "extend the period" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.l_bound, str(error))
            self.update_ui_for_invalid_input(self.ui_elements.u_bound, str(error))
            self.update_ui_for_invalid_input(self.ui_elements.n_elements, str(error))
            self.update_ui_for_invalid_input(self.ui_elements.n_groups, str(error))
        if "length of sequence" in str(error).lower():
            self.update_ui_for_invalid_input(self.ui_elements.n_elements, str(error))

    def update_ui_for_invalid_input(self, field, message):
        """
        Updates the UI elements for invalid input.
        """

        field.setStyleSheet("color: red; border: 1px solid red;")
        field.setToolTip(message)

    def get_holidays(self) -> list[date] | None:
        """
        Exclude bank holidays from the date generation.
        """

        # Check button state, since checking and unchecking the button trigger the same signal
        if not self.ui_elements.exclude_bank_holidays.isChecked():
            self.list_public_holidays = None
            return

        # Get the public holidays in the period
        self.public_holidays.set_period(
            self.ui_elements.l_bound.date().toPyDate().year,
            self.ui_elements.u_bound.date().toPyDate().year,
        )

        if self.loading_window.isVisible():
            self.loading_window.close()
        else:
            self.loading_window.show()

        # animate a loading animation in the progress bar while the public holidays are being fetched
        animation = QPropertyAnimation(self.loading_window.progressBar, b"value")
        animation.setDuration(3600)
        animation.setStartValue(0)
        animation.setEndValue(100)
        animation.start(policy=QPropertyAnimation.DeletionPolicy.KeepWhenStopped)

        public_holidays = self.public_holidays.return_list_public_holidays()

        # Stop the loading animation
        if public_holidays is not None:
            animation.stop()
            self.loading_window.close()

        # Stop the loading animation after 30000ms and display an error message
        else:
            animation.stop()
            self.loading_window.close()
            self.loading_window.progressBar.setValue(100)
            self.loading_window.progressBar.setStyleSheet("background-color: red;")
            self.loading_window.progressBar.setTextVisible(True)
            self.loading_window.progressBar.setFormat("Failed to fetch public holidays")
            self.loading_window.show()

        return public_holidays

    def generate_sequence(self):

        # Reset the UI elements
        self.reset_ui()

        self.check_input_fields()

        # Check if the user has an active session and set the seed
        if self.seed is None:
            self.ui_elements.btn_seed_dates.click()

        date_sequence = self.rdg.generate_and_return_sequence(
            self.ui_elements.l_bound.date().toPyDate(),
            self.ui_elements.u_bound.date().toPyDate(),
            (self.ui_elements.n_elements.value() * self.ui_elements.n_groups.value()),
            holidays=self.get_holidays(),
            exclude_saturdays=self.ui_elements.exclude_saturdays.isChecked(),
            exclude_sundays=self.ui_elements.exclude_sundays.isChecked(),
        )

        return date_sequence

    def group_sequence(self, date_sequence):

        # Sort the date sequence based on the user's preference
        if self.ui_elements.ascending_order.isChecked():
            date_sequence = sorted(date_sequence)
        elif self.ui_elements.descending_order.isChecked():
            date_sequence = sorted(date_sequence, reverse=True)
        elif self.ui_elements.original_order.isChecked():
            date_sequence = date_sequence

        date_output = {}

        if self.ui_elements.n_groups.value() > 1:
            s = 0
            for i in range(self.ui_elements.n_groups.value()):

                date_output[f"group_{i + 1}"] = date_sequence[
                    s : s + self.ui_elements.n_elements.value()
                ]
                s += self.ui_elements.n_elements.value()

        else:
            date_output["group_1"] = date_sequence

        return date_output

    def generate_emit_sequence(self):

        try:
            date_sequence = self.generate_sequence()

            date_output = self.group_sequence(date_sequence)

            if self.output_window.isVisible():
                self.output_window.close()
            else:
                self.output_window.show()

            # print the date_sequence
            self.output_window.output_element.clear()
            self.output_window.output_element.append(
                self.ui_elements.sequence_name.text()
            )
            self.output_window.output_element.append("")

            for group, dates in date_output.items():
                self.output_window.output_element.append(f"{group}: {dates}")

            self.output_window.show()

        except InvalidInputError as e:
            self.update_ui_for_errors(e)
