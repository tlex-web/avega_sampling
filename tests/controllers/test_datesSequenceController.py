import pytest
from PyQt6.QtCore import QDate, QPropertyAnimation
from PyQt6.QtWidgets import QProgressBar
from datetime import date
from unittest.mock import create_autospec

from fixtures import (
    ui_elements_dates as ui_elements,
    public_holidays,
    output_window,
    loading_window,
)

from controllers.datesSequenceController import (
    DatesSequenceController,
)
from library.custom_errors.InvalidInputError import InvalidInputError


def test_clear_fields(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)
    controller.clear_fields()

    assert ui_elements.sequence_name.clear.called
    assert ui_elements.sequence_name.setPlaceholderText.called_with("sequence 1")
    assert ui_elements.l_bound.setDate.called_with(ui_elements.l_bound.minimumDate())
    assert ui_elements.u_bound.setDate.called_with(ui_elements.u_bound.maximumDate())
    assert ui_elements.n_groups.setValue.called_with(1)
    assert ui_elements.n_elements.setValue.called_with(0)
    assert ui_elements.original_order.setChecked.called_with(True)
    assert ui_elements.ascending_order.setChecked.called_with(False)
    assert ui_elements.descending_order.setChecked.called_with(False)
    assert ui_elements.sequence_name.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements.l_bound.setStyleSheet.called_with("color: black; border: none;")
    assert ui_elements.u_bound.setStyleSheet.called_with("color: black; border: none;")
    assert ui_elements.n_groups.setStyleSheet.called_with("color: black; border: none;")
    assert ui_elements.n_elements.setStyleSheet.called_with(
        "color: black; border: none;"
    )


def test_reset_ui(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)
    controller.reset_ui()

    assert ui_elements.sequence_name.setToolTip("")
    assert ui_elements.l_bound.setToolTip("")
    assert ui_elements.u_bound.setToolTip("")
    assert ui_elements.n_groups.setToolTip("")
    assert ui_elements.n_elements.setToolTip("")
    assert ui_elements.sequence_name.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements.l_bound.setStyleSheet.called_with("color: black; border: none;")
    assert ui_elements.u_bound.setStyleSheet.called_with("color: black; border: none;")
    assert ui_elements.n_groups.setStyleSheet.called_with("color: black; border: none;")
    assert ui_elements.n_elements.setStyleSheet.called_with(
        "color: black; border: none;"
    )


test_cases = {
    "1": {
        "input": {
            "sequence_name": "",
            "l_bound": QDate(2022, 1, 1),
            "u_bound": QDate(2022, 1, 4),
            "n_groups": 1,
            "n_elements": 4,
            "original_order": True,
            "ascending_order": False,
            "descending_order": False,
        },
        "expected": "Sequence name cannot be empty",
    },
    "2": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": QDate(2022, 1, 4),
            "u_bound": QDate(2022, 1, 1),
            "n_groups": 2,
            "n_elements": 2,
            "original_order": False,
            "ascending_order": True,
            "descending_order": False,
        },
        "expected": "Lower bound must be less than upper bound",
    },
    "3": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": QDate(2022, 1, 1),
            "u_bound": QDate(2022, 1, 4),
            "n_groups": 0,
            "n_elements": 0,
            "original_order": False,
            "ascending_order": False,
            "descending_order": False,
        },
        "expected": "Number of groups must be greater than 0",
    },
    "4": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": QDate(2022, 1, 1),
            "u_bound": QDate(2022, 1, 4),
            "n_groups": 2,
            "n_elements": 0,
            "original_order": False,
            "ascending_order": False,
            "descending_order": False,
        },
        "expected": "Number of elements must be greater than 0",
    },
    "5": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": QDate(2022, 1, 1),
            "u_bound": QDate(2022, 1, 2),
            "n_groups": 2,
            "n_elements": 2,
            "original_order": False,
            "ascending_order": False,
            "descending_order": False,
        },
        "expected": "Extend the period or reduce the number of elements or groups",
    },
}


def test_check_input_fields(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)

    for key, value in test_cases.items():
        print(
            f"Running test case {key} with input {value['input']} and expected {value['expected']}"
        )
        ui_elements.sequence_name.text.return_value = value["input"]["sequence_name"]
        ui_elements.l_bound.date.return_value = value["input"]["l_bound"]
        ui_elements.u_bound.date.return_value = value["input"]["u_bound"]
        ui_elements.n_groups.value.return_value = value["input"]["n_groups"]
        ui_elements.n_elements.value.return_value = value["input"]["n_elements"]
        ui_elements.original_order.isChecked.return_value = value["input"][
            "original_order"
        ]
        ui_elements.ascending_order.isChecked.return_value = value["input"][
            "ascending_order"
        ]
        ui_elements.descending_order.isChecked.return_value = value["input"][
            "descending_order"
        ]

        with pytest.raises(InvalidInputError, match=value["expected"]):
            controller.check_input_fields()


def test_update_ui_for_errors(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)
    error = InvalidInputError("Sequence name cannot be empty")
    controller.update_ui_for_errors(error)
    assert ui_elements.sequence_name.styleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.sequence_name.toolTip.called_with(str(error))


##### Test currently failing #####
# proposed fix: create a functional mock for the QPropertyAnimation class and its properties
def test_get_holidays_exclude_bank_holidays_checked(
    ui_elements,
    mocker,
    public_holidays,
    output_window,
    loading_window,
):
    # Create a mock for QProgressBar
    progressBarMock = create_autospec(QProgressBar, instance=True)

    # Ensure the loading_window mock has a progressBar attribute
    if not hasattr(loading_window, "progressBar"):
        loading_window.progressBar = progressBarMock

    loading_window.progressBar.value.return_value = 0

    mocker.patch.object(public_holidays, "set_period")
    mocker.patch.object(
        public_holidays, "return_list_public_holidays", return_value=[date(2022, 1, 1)]
    )

    controller = DatesSequenceController(ui_elements, output_window, loading_window)
    controller.public_holidays = public_holidays
    ui_elements.exclude_bank_holidays.isChecked.return_value = True

    assert (
        loading_window.progressBar
    )  # Add this line to access the progressBar attribute
    holidays = controller.get_holidays()

    assert holidays == [date(2022, 1, 1)]
    public_holidays.set_period.assert_called_once_with(2022, 2022)
    public_holidays.return_list_public_holidays.assert_called_once()


def test_get_holidays_exclude_bank_holidays_not_checked(
    ui_elements, output_window, loading_window, public_holidays, mocker
):
    mocker.patch.object(public_holidays, "set_period")

    controller = DatesSequenceController(ui_elements, output_window, loading_window)
    controller.public_holidays = public_holidays
    ui_elements.exclude_bank_holidays.isChecked.return_value = False

    holidays = controller.get_holidays()

    assert holidays is None
    public_holidays.set_period.assert_not_called()


##### Test currently failing #####
# proposed fix: create a functional mock for the QPropertyAnimation class and its properties
def test_get_holidays_loading_window_visible(
    ui_elements, output_window, loading_window, public_holidays, mocker
):
    mocker.patch.object(public_holidays, "set_period")
    mocker.patch.object(
        public_holidays, "return_list_public_holidays", return_value=None
    )
    mocker.patch.object(QPropertyAnimation, "start")
    mocker.patch.object(QPropertyAnimation, "stop")
    mocker.patch.object(loading_window, "show")
    mocker.patch.object(loading_window, "close")

    controller = DatesSequenceController(ui_elements, output_window, loading_window)
    controller.public_holidays = public_holidays
    ui_elements.exclude_bank_holidays.isChecked.return_value = True
    loading_window.isVisible.return_value = True

    holidays = controller.get_holidays()

    assert holidays is None
    public_holidays.set_period.assert_called_once_with(2022, 2022)
    public_holidays.return_list_public_holidays.assert_called_once()
    loading_window.show.assert_not_called()
    loading_window.close.assert_called_once()
    QPropertyAnimation.start.assert_not_called()
    QPropertyAnimation.stop.assert_not_called()


##### Test currently failing #####
# proposed fix: create a functional mock for the QPropertyAnimation class and its properties
def test_get_holidays_loading_window_not_visible(
    ui_elements, output_window, loading_window, public_holidays, mocker
):
    mocker.patch.object(public_holidays, "set_period")
    mocker.patch.object(
        public_holidays, "return_list_public_holidays", return_value=None
    )
    mocker.patch.object(QPropertyAnimation, "start")
    mocker.patch.object(QPropertyAnimation, "stop")
    mocker.patch.object(loading_window, "show")
    mocker.patch.object(loading_window, "close")

    controller = DatesSequenceController(ui_elements, output_window, loading_window)
    controller.public_holidays = public_holidays
    ui_elements.exclude_bank_holidays.isChecked.return_value = True
    loading_window.isVisible.return_value = False

    holidays = controller.get_holidays()

    assert holidays is None
    public_holidays.set_period.assert_called_once_with(2022, 2022)
    public_holidays.return_list_public_holidays.assert_called_once()
    loading_window.show.assert_not_called()
    loading_window.close.assert_called_once()
    QPropertyAnimation.start.assert_not_called()
    QPropertyAnimation.stop.assert_not_called()


##### Test currently failing #####
# proposed fix: create a functional mock for the QPropertyAnimation class and its properties
def test_get_holidays_loading_window_visible_with_error(
    ui_elements, output_window, loading_window, public_holidays, mocker
):
    mocker.patch.object(public_holidays, "set_period")
    mocker.patch.object(
        public_holidays, "return_list_public_holidays", return_value=None
    )
    mocker.patch.object(QPropertyAnimation, "start")
    mocker.patch.object(QPropertyAnimation, "stop")
    mocker.patch.object(loading_window, "show")
    mocker.patch.object(loading_window, "close")
    mocker.patch.object(loading_window.progressBar, "setValue")
    mocker.patch.object(loading_window.progressBar, "setStyleSheet")
    mocker.patch.object(loading_window.progressBar, "setTextVisible")
    mocker.patch.object(loading_window.progressBar, "setFormat")

    controller = DatesSequenceController(ui_elements, output_window, loading_window)
    controller.public_holidays = public_holidays
    ui_elements.exclude_bank_holidays.isChecked.return_value = True
    loading_window.isVisible.return_value = True

    holidays = controller.get_holidays()

    assert holidays is None
    public_holidays.set_period.assert_called_once_with(2022, 2022)
    public_holidays.return_list_public_holidays.assert_called_once()
    loading_window.show.assert_not_called()
    loading_window.close.assert_called_once()
    QPropertyAnimation.start.assert_not_called()
    QPropertyAnimation.stop.assert_called_once()
    loading_window.progressBar.setValue.assert_called_once_with(100)
    loading_window.progressBar.setStyleSheet.assert_called_once_with(
        "background-color: red;"
    )
    loading_window.progressBar.setTextVisible.assert_called_once_with(True)
    loading_window.progressBar.setFormat.assert_called_once_with(
        "Failed to fetch public holidays"
    )


def test_generate_sequence(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)

    controller.rdg.set_seed(123)
    # create dummy values
    ui_elements.l_bound.date.return_value = QDate(2022, 1, 1)
    ui_elements.u_bound.date.return_value = QDate(2022, 1, 4)
    ui_elements.n_groups.value.return_value = 1
    ui_elements.n_elements.value.return_value = 4
    ui_elements.ascending_order.isChecked.return_value = False
    ui_elements.descending_order.isChecked.return_value = False
    ui_elements.original_order.isChecked.return_value = True
    ui_elements.exclude_bank_holidays.isChecked.return_value = False
    ui_elements.exclude_saturdays.isChecked.return_value = False
    ui_elements.exclude_sundays.isChecked.return_value = False

    sequence = controller.generate_sequence()
    assert sequence == ["2022-01-03", "2022-01-02", "2022-01-01", "2022-01-01"]


def test_group_sequence_asc(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)
    date_sequence = [
        date(2022, 1, 4),
        date(2022, 1, 2),
        date(2022, 1, 3),
        date(2022, 1, 1),
    ]
    ui_elements.ascending_order.isChecked.return_value = True
    ui_elements.descending_order.isChecked.return_value = False
    ui_elements.original_order.isChecked.return_value = False
    ui_elements.n_groups.value.return_value = 1
    ui_elements.n_elements.value.return_value = 4
    date_output = controller.group_sequence(date_sequence)
    assert date_output == {
        "group_1": [
            date(2022, 1, 1),
            date(2022, 1, 2),
            date(2022, 1, 3),
            date(2022, 1, 4),
        ]
    }


def test_group_sequence_desc(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)
    date_sequence = [
        date(2022, 1, 3),
        date(2022, 1, 4),
        date(2022, 1, 2),
        date(2022, 1, 1),
    ]
    ui_elements.descending_order.isChecked.return_value = True
    ui_elements.ascending_order.isChecked.return_value = False
    ui_elements.original_order.isChecked.return_value = False
    ui_elements.n_groups.value.return_value = 1
    ui_elements.n_elements.value.return_value = 4
    date_output = controller.group_sequence(date_sequence)
    assert date_output == {
        "group_1": [
            date(2022, 1, 4),
            date(2022, 1, 3),
            date(2022, 1, 2),
            date(2022, 1, 1),
        ]
    }


def test_group_sequence_original(ui_elements):
    controller = DatesSequenceController(ui_elements, None, None)
    date_sequence = [
        date(2022, 1, 2),
        date(2022, 1, 4),
        date(2022, 1, 1),
        date(2022, 1, 3),
    ]
    ui_elements.ascending_order.isChecked.return_value = False
    ui_elements.descending_order.isChecked.return_value = False
    ui_elements.original_order.isChecked.return_value = True
    ui_elements.n_groups.value.return_value = 1
    ui_elements.n_elements.value.return_value = 4
    date_output = controller.group_sequence(date_sequence)
    assert date_output == {
        "group_1": [
            date(2022, 1, 2),
            date(2022, 1, 4),
            date(2022, 1, 1),
            date(2022, 1, 3),
        ]
    }


#### Test currently failing ####
# proposed fix: mock methods executed inside of handle_generate_sequence_btn()
def test_handle_generate_sequence_btn(ui_elements, output_window):
    controller = DatesSequenceController(ui_elements, output_window, None)
    controller.handle_generate_sequence_btn()
    assert output_window.isVisible


#### Test currently failing ####
# proposed fix: mock methods executed inside of handle_generate_sequence_btn()
def test_handle_generate_sequence_btn_with_error(ui_elements, output_window):
    controller = DatesSequenceController(ui_elements, output_window, None)
    controller.update_ui_for_errors(InvalidInputError("Invalid input"))
    controller.handle_generate_sequence_btn()
    assert not output_window.isVisible


#### Test currently failing ####
# proposed fix: mock methods executed inside of handle_generate_sequence_btn()
def test_handle_generate_sequence_btn_with_loading_window(
    ui_elements, output_window, loading_window
):
    controller = DatesSequenceController(ui_elements, output_window, loading_window)
    controller.handle_generate_sequence_btn()
    assert loading_window.isVisible


#### Test currently failing ####
# proposed fix: mock methods executed inside of handle_generate_sequence_btn()
def test_handle_generate_sequence_btn_with_invalid_input_error(
    ui_elements, output_window
):
    controller = DatesSequenceController(ui_elements, output_window, None)
    controller.update_ui_for_errors(InvalidInputError("Invalid input"))
    controller.handle_generate_sequence_btn()
    assert not output_window.isVisible


#### Test currently failing ####
# proposed fix: mock methods executed inside of handle_generate_sequence_btn()
def test_handle_generate_sequence_btn_with_other_error(ui_elements, output_window):
    controller = DatesSequenceController(ui_elements, output_window, None)
    controller.update_ui_for_errors(Exception("Other error"))
    controller.handle_generate_sequence_btn()
    assert not output_window.isVisible
