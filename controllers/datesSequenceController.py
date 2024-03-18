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

from utils.PCGRNG import PCGRNG
from utils.FetchPublicHolidays import FetchPublicHolidays

from models.Seed import Seed
from models.User import User
from config import SESSION_NAME


class DatesSequenceController:

    def __init__(
        self,
        btn_generate_dates: QPushButton,
        btn_clear_dates: QPushButton,
        exclude_bank_holidays: QCheckBox,
        exclude_saturdays: QCheckBox,
        exclude_sundays: QCheckBox,
        sequence_name: QLineEdit,
        l_bound: QDateEdit,
        u_bound: QDateEdit,
        label_lbound: QLabel,
        label_ubound: QLabel,
        exclude_dates: QGroupBox,
        n_groups: QSpinBox,
        label_n_groups: QLabel,
        n_elements: QSpinBox,
        label_n_elements: QLabel,
        original_order: QRadioButton,
        ascending_order: QRadioButton,
        descending_order: QRadioButton,
        output_window,
        loading_window,
    ) -> None:
        """
        Initializes the number sequence controller.
        """
        self.btn_generate_dates = btn_generate_dates
        self.btn_clear_dates = btn_clear_dates
        self.exclude_bank_holidays = exclude_bank_holidays
        self.exclude_saturdays = exclude_saturdays
        self.exclude_sundays = exclude_sundays
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
        self.original_order = original_order
        self.ascending_order = ascending_order
        self.descending_order = descending_order
        self.output_window = output_window
        self.loading_window = loading_window
        self.seed_model = Seed()
        self.user_model = User()
        self.fetch_public_holidays = FetchPublicHolidays()
        self.pcgrng = PCGRNG()
        self.public_holidays = None

        # Setup signals and slots for number sequence-related actions
        self.exclude_bank_holidays.clicked.connect(self.exclude_holidays)
        self.btn_clear_dates.clicked.connect(self.clear_dates)
        self.btn_generate_dates.clicked.connect(self.generate_dates)

    def exclude_holidays(self):
        """
        Exclude bank holidays from the date generation.
        """

        # Get the period between the lower and upper bounds
        l_bound = self.l_bound.date().toPyDate().year
        u_bound = self.u_bound.date().toPyDate().year

        # Get the public holidays in the period
        self.fetch_public_holidays.set_period(l_bound, u_bound)

        if self.loading_window.isVisible():
            self.loading_window.close()
        else:
            self.loading_window.show()

        # animate a loading animation in the progress bar while the public holidays are being fetched
        animation = QPropertyAnimation(self.loading_window.progressBar, b"value")
        animation.setDuration(1000)
        animation.setStartValue(0)
        animation.setLoopCount(-1)
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
            self.loading_window.loading_bar.setValue(100)
            self.loading_window.loading_bar.setStyleSheet("background-color: red;")
            self.loading_window.loading_bar.setTextVisible(True)
            self.loading_window.loading_bar.setFormat("Failed to fetch public holidays")
            self.loading_window.show()

        self.public_holidays = public_holidays

    def clear_dates(self):
        """
        Clear the input fields for date generation and reset placeholder values.
        """

        # Clear the input fields and reset placeholder values
        self.sequence_name.clear()
        self.sequence_name.setPlaceholderText("Enter sequence name")

        self.l_bound.clear()
        self.l_bound.setDate(self.l_bound.minimumDate())

        self.u_bound.clear()
        self.u_bound.setDate(self.u_bound.maximumDate())

        self.exclude_dates.clearMask()

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

    def generate_dates(self):
        """
        Generate random dates based on the input fields and displays them in the output window.
        """
        # get the values from the input fields and convert them to the correct type
        sequence_name = (
            self.sequence_name.text()
            if self.sequence_name.text() != ""
            else "sequence 1"
        )
        l_bound = self.l_bound.date().toPyDate()
        u_bound = self.u_bound.date().toPyDate()

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

        # Check if the user wants to exclude certain days
        excluded_days = []
        if self.exclude_saturdays.isChecked():
            excluded_days.append(5)  # Saturday
        if self.exclude_sundays.isChecked():
            excluded_days.append(6)  # Sunday

        dates = []  # Initialize the "dates" variable

        if (
            self.exclude_bank_holidays.isChecked()
            and self.public_holidays is not None
            and len(self.public_holidays) > 0
        ):
            if self.public_holidays is not None:
                public_holidays = [holiday["date"] for holiday in self.public_holidays]
                dates = [date for date in dates if date not in public_holidays]
            else:
                self.exclude_bank_holidays.setStyleSheet(
                    "color: red; border: 1px solid red;"
                )
                self.exclude_bank_holidays.setToolTip("Failed to fetch public holidays")
                return

        # Exclude the selected days
        dates = [date for date in dates if date.weekday() not in excluded_days]

        # Set the seed for the random date generator

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

        pcg = PCGRNG(seed_value)

        dates = pcg.get_unique_random_sequence(1, len(dates), n_elements)
        # Fix the order and display error messages on the UI
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
