import pytest
from PyQt6.QtWidgets import QPushButton, QLabel, QRadioButton, QSpinBox, QLineEdit
from unittest.mock import Mock
from controllers.numberSequenceController import (
    NumberSequenceController,
    UIElementsNumberSequence,
)
from library.custom_errors.InvalidInputError import InvalidInputError


@pytest.fixture
def ui_elements():
    return UIElementsNumberSequence(
        btn_generate_numbers=Mock(spec=QPushButton),
        btn_seed_numbers=Mock(spec=QPushButton),
        btn_clear_numbers=Mock(spec=QPushButton),
        sequence_name=Mock(spec=QLineEdit),
        l_bound=Mock(spec=QSpinBox),
        u_bound=Mock(spec=QSpinBox),
        label_lbound=Mock(spec=QLabel),
        label_ubound=Mock(spec=QLabel),
        n_groups=Mock(spec=QSpinBox),
        label_n_groups=Mock(spec=QLabel),
        n_elements=Mock(spec=QSpinBox),
        label_n_elements=Mock(spec=QLabel),
        original_order=Mock(spec=QRadioButton),
        ascending_order=Mock(spec=QRadioButton),
        descending_order=Mock(spec=QRadioButton),
    )


@pytest.fixture
def output_window():
    return Mock()


def test_clear_fields(ui_elements, output_window):
    controller = NumberSequenceController(ui_elements, output_window=output_window)
    controller.clear_fields()

    assert ui_elements.sequence_name.clear.called
    assert ui_elements.sequence_name.setPlaceholderText.called_with("sequence 1")
    assert ui_elements.l_bound.clear.called
    assert ui_elements.l_bound.setValue.called_with(0)
    assert ui_elements.u_bound.clear.called
    assert ui_elements.u_bound.setValue.called_with(0)
    assert ui_elements.n_groups.clear.called
    assert ui_elements.n_groups.setValue.called_with(1)
    assert ui_elements.n_elements.clear.called
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
    assert ui_elements.sequence_name.setToolTip.called_with("")
    assert ui_elements.l_bound.setToolTip.called_with("")
    assert ui_elements.u_bound.setToolTip.called_with("")
    assert ui_elements.n_groups.setToolTip.called_with("")
    assert ui_elements.n_elements.setToolTip.called_with("")


def test_reset_ui(ui_elements, output_window):
    controller = NumberSequenceController(ui_elements, output_window=output_window)
    controller.reset_ui()

    assert ui_elements.sequence_name.setStyleSheet.called_with("")
    assert ui_elements.sequence_name.setToolTip.called_with("")
    assert ui_elements.l_bound.setStyleSheet.called_with("")
    assert ui_elements.l_bound.setToolTip.called_with("")
    assert ui_elements.u_bound.setStyleSheet.called_with("")
    assert ui_elements.u_bound.setToolTip.called_with("")
    assert ui_elements.n_groups.setStyleSheet.called_with("")
    assert ui_elements.n_groups.setToolTip.called_with("")
    assert ui_elements.n_elements.setStyleSheet.called_with("")
    assert ui_elements.n_elements.setToolTip.called_with("")


test_cases = {
    "1": {
        "input": {
            "sequence_name": "",
            "l_bound": 0,
            "u_bound": 0,
            "n_groups": 0,
            "n_elements": 0,
        },
        "expected": "Sequence name cannot be empty",
    },
    "2": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": 0,
            "u_bound": 0,
            "n_groups": 0,
            "n_elements": 0,
        },
        "expected": "Lower bound must be greater than 0",
    },
    "3": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": 5,
            "u_bound": 0,
            "n_groups": 0,
            "n_elements": 0,
        },
        "expected": "Upper bound must be greater than 0",
    },
    "4": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": 1,
            "u_bound": 3,
            "n_groups": 0,
            "n_elements": 0,
        },
        "expected": "Number of groups must be greater than 0",
    },
    "5": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": 1,
            "u_bound": 3,
            "n_groups": 2,
            "n_elements": 0,
        },
        "expected": "Number of elements must be greater than 0",
    },
    "6": {
        "input": {
            "sequence_name": "sequence 1",
            "l_bound": 3,
            "u_bound": 5,
            "n_groups": 2,
            "n_elements": 3,
        },
        "expected": "The range of numbers must be greater than the number of elements",
    },
}


def test_check_input_fields(ui_elements, output_window):
    controller = NumberSequenceController(ui_elements, output_window=output_window)

    for key, value in test_cases.items():
        print(
            f"Running test case {key} with input {value['input']} and expected {value['expected']}"
        )
        ui_elements.sequence_name.text.return_value = value["input"]["sequence_name"]
        ui_elements.l_bound.value.return_value = value["input"]["l_bound"]
        ui_elements.u_bound.value.return_value = value["input"]["u_bound"]
        ui_elements.n_groups.value.return_value = value["input"]["n_groups"]
        ui_elements.n_elements.value.return_value = value["input"]["n_elements"]

        with pytest.raises(InvalidInputError, match=value["expected"]):
            controller.check_input_fields()


def test_update_ui_for_errors(ui_elements):
    controller = NumberSequenceController(ui_elements, output_window=None)

    error = InvalidInputError("Sequence name cannot be empty")
    controller.update_ui_for_errors(error)
    assert ui_elements.sequence_name.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.sequence_name.setToolTip.called_with(str(error))

    error = InvalidInputError("Lower bound must be less than the upper bound")
    controller.update_ui_for_errors(error)
    assert ui_elements.l_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.l_bound.setToolTip.called_with(str(error))

    error = InvalidInputError("Upper bound must be greater than 0")
    controller.update_ui_for_errors(error)
    assert ui_elements.u_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.u_bound.setToolTip.called_with(str(error))

    error = InvalidInputError("Number of groups must be greater than 0")
    controller.update_ui_for_errors(error)
    assert ui_elements.n_groups.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.n_groups.setToolTip.called_with(str(error))

    error = InvalidInputError("Number of elements must be greater than 0")
    controller.update_ui_for_errors(error)
    assert ui_elements.n_elements.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.n_elements.setToolTip.called_with(str(error))

    error = InvalidInputError(
        "The range of numbers must be greater than the number of elements"
    )
    controller.update_ui_for_errors(error)
    assert ui_elements.l_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.l_bound.setToolTip.called_with(str(error))
    assert ui_elements.u_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements.u_bound.setToolTip.called_with(str(error))

    error = InvalidInputError("Sequence generation failed")
    controller.update_ui_for_errors(error)
    assert ui_elements.l_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
