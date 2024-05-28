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

from controllers.library.baseSequenceController import BaseSequenceController

from models.Generators import RandomDatesSequenceGenerator
from utils.FetchPublicHolidays import FetchPublicHolidays

from models.Seed import Seed
from models.User import User
from config import SESSION_NAME


class UIElementsDatesSequence(NamedTuple):
    btn_generate_dates: QPushButton
    btn_clear_dates: QPushButton
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


## still issues with exclusion of dates and bank holidays


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
        self.ui_elements = ui_elements
        self.output_window = output_window
        self.loading_window = loading_window
        self.seed_model = Seed()
        self.user_model = User()
        self.fetch_public_holidays = FetchPublicHolidays()
        self.rdg = RandomDatesSequenceGenerator()
        self.public_holidays = None

        # Setup signals and slots for number sequence-related actions
        self.ui_elements.exclude_bank_holidays.clicked.connect(self.get_holidays)
        self.ui_elements.btn_clear_dates.clicked.connect(self.clear_fields)
        self.ui_elements.btn_generate_dates.clicked.connect(self.print_sequence)

        # Setup signals and slots for seed-related actions
        # We must ignore the type of the signal, since the signal is overloaded
        self.rdg.error_rdg_generation.connect(self.error_rdg_generation)  # type: ignore

    def error_rdg_generation(self, error_message):
        """
        Displays an error message if the random date generation fails.
        """

        self.output_window.output_element.clear()
        self.output_window.output_element.append("An error occurred")
        self.output_window.output_element.append(error_message)
        self.output_window.show()

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

        self.rdg.set_seed(seed_value)

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

    def check_input_fields(self):
        # Check if the values are valid
        if self.ui_elements.sequence_name.text() == "":
            self.ui_elements.sequence_name.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.sequence_name.setToolTip("Enter a sequence name")
            return
        else:
            self.ui_elements.sequence_name.setStyleSheet("color: black; border: none;")
        if (
            self.ui_elements.l_bound.date().toPyDate()
            >= self.ui_elements.u_bound.date().toPyDate()
        ):
            self.ui_elements.l_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.l_bound.setToolTip(
                "Lower bound must be greater than lower bound"
            )
            self.ui_elements.u_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.u_bound.setToolTip(
                "Upper bound must be greater than lower bound"
            )
            return
        else:
            self.ui_elements.l_bound.setStyleSheet("color: black; border: none;")
            self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")

        if self.ui_elements.n_groups.value() < 1:
            self.ui_elements.n_groups.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_groups.setToolTip(
                "Number of groups must be greater than 0"
            )
            return
        else:
            self.ui_elements.n_groups.setStyleSheet("color: black; border: none;")

        if self.ui_elements.n_elements.value() < 1:
            self.ui_elements.n_elements.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_elements.setToolTip(
                "Number of elements must be greater than 0"
            )
            return
        else:
            self.ui_elements.n_elements.setStyleSheet("color: black; border: none;")

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
            self.ui_elements.n_elements.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_elements.setToolTip(
                "Extend the period or reduce the number of elements"
            )
            self.ui_elements.n_groups.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.n_groups.setToolTip(
                "Extend the period or reduce the number of groups"
            )
            self.ui_elements.l_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.l_bound.setToolTip(
                "Extend the period or reduce the number of groups"
            )
            self.ui_elements.u_bound.setStyleSheet("color: red; border: 1px solid red;")
            self.ui_elements.u_bound.setToolTip(
                "Extend the period or reduce the number of groups"
            )
            return
        else:
            self.ui_elements.n_elements.setStyleSheet("color: black; border: none;")
            self.ui_elements.n_groups.setStyleSheet("color: black; border: none;")
            self.ui_elements.l_bound.setStyleSheet("color: black; border: none;")
            self.ui_elements.u_bound.setStyleSheet("color: black; border: none;")

    def get_holidays(self) -> list[date] | None:
        """
        Exclude bank holidays from the date generation.
        """

        # Check button state, since checking and unchecking the button trigger the same signal
        if not self.ui_elements.exclude_bank_holidays.isChecked():
            self.public_holidays = None
            return

        # Get the public holidays in the period
        self.fetch_public_holidays.set_period(
            self.ui_elements.l_bound.date().toPyDate().year,
            self.ui_elements.u_bound.date().toPyDate().year,
        )

        if self.loading_window.isVisible():
            self.loading_window.close()
        else:
            self.loading_window.show()

        # animate a loading animation in the progress bar while the public holidays are being fetched
        animation = QPropertyAnimation(self.loading_window.progressBar, b"value")
        animation.setDuration(30000)
        animation.setStartValue(0)
        animation.setEndValue(100)
        animation.start()

        public_holidays = self.fetch_public_holidays.get_public_holidays()

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

        self.check_input_fields()

        try:

            # Set the seed for the random date generator
            self.check_session()

            date_sequence = self.rdg.generate_and_return_sequence(
                self.ui_elements.l_bound.date().toPyDate(),
                self.ui_elements.u_bound.date().toPyDate(),
                (
                    self.ui_elements.n_elements.value()
                    * self.ui_elements.n_groups.value()
                ),
                holidays=self.get_holidays(),
                exclude_saturdays=self.ui_elements.exclude_saturdays.isChecked(),
                exclude_sundays=self.ui_elements.exclude_sundays.isChecked(),
            )
        except ValueError as e:
            self.ui_elements.btn_generate_dates.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.btn_generate_dates.setToolTip(str(e))
            return
        except Exception as e:
            self.ui_elements.btn_generate_dates.setStyleSheet(
                "color: red; border: 1px solid red;"
            )
            self.ui_elements.btn_generate_dates.setToolTip(str(e))
            return

        return date_sequence

    def print_sequence(self):

        date_sequence = self.generate_sequence()

        if date_sequence is None:
            return

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

        if self.output_window.isVisible():
            self.output_window.close()
        else:
            self.output_window.show()

        # print the date_sequence
        self.output_window.output_element.clear()
        self.output_window.output_element.append(self.ui_elements.sequence_name.text())
        self.output_window.output_element.append("")

        for group, dates in date_output.items():
            self.output_window.output_element.append(group)
            for date in dates:
                self.output_window.output_element.append(date.strftime("%Y-%m-%d"))
            self.output_window.output_element.append("")
