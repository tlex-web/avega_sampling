import pytest

from fixtures import ui_elements_number, output_window

from controllers.numberSequenceController import NumberSequenceController
from library.custom_errors.InvalidInputError import InvalidInputError


def test_clear_fields(ui_elements_number, output_window):
    controller = NumberSequenceController(
        ui_elements_number, output_window=output_window
    )
    controller.clear_fields()

    assert ui_elements_number.sequence_name.clear.called
    assert ui_elements_number.sequence_name.setPlaceholderText.called_with("sequence 1")
    assert ui_elements_number.l_bound.clear.called
    assert ui_elements_number.l_bound.setValue.called_with(0)
    assert ui_elements_number.u_bound.clear.called
    assert ui_elements_number.u_bound.setValue.called_with(0)
    assert ui_elements_number.n_groups.clear.called
    assert ui_elements_number.n_groups.setValue.called_with(1)
    assert ui_elements_number.n_elements.clear.called
    assert ui_elements_number.n_elements.setValue.called_with(0)
    assert ui_elements_number.original_order.setChecked.called_with(True)
    assert ui_elements_number.ascending_order.setChecked.called_with(False)
    assert ui_elements_number.descending_order.setChecked.called_with(False)
    assert ui_elements_number.sequence_name.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements_number.l_bound.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements_number.u_bound.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements_number.n_groups.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements_number.n_elements.setStyleSheet.called_with(
        "color: black; border: none;"
    )
    assert ui_elements_number.sequence_name.setToolTip.called_with("")
    assert ui_elements_number.l_bound.setToolTip.called_with("")
    assert ui_elements_number.u_bound.setToolTip.called_with("")
    assert ui_elements_number.n_groups.setToolTip.called_with("")
    assert ui_elements_number.n_elements.setToolTip.called_with("")


def test_reset_ui(ui_elements_number, output_window):
    controller = NumberSequenceController(
        ui_elements_number, output_window=output_window
    )
    controller.reset_ui()

    assert ui_elements_number.sequence_name.setStyleSheet.called_with("")
    assert ui_elements_number.sequence_name.setToolTip.called_with("")
    assert ui_elements_number.l_bound.setStyleSheet.called_with("")
    assert ui_elements_number.l_bound.setToolTip.called_with("")
    assert ui_elements_number.u_bound.setStyleSheet.called_with("")
    assert ui_elements_number.u_bound.setToolTip.called_with("")
    assert ui_elements_number.n_groups.setStyleSheet.called_with("")
    assert ui_elements_number.n_groups.setToolTip.called_with("")
    assert ui_elements_number.n_elements.setStyleSheet.called_with("")
    assert ui_elements_number.n_elements.setToolTip.called_with("")


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


def test_check_input_fields(ui_elements_number, output_window):
    controller = NumberSequenceController(
        ui_elements_number, output_window=output_window
    )

    for key, value in test_cases.items():
        print(
            f"Running test case {key} with input {value['input']} and expected {value['expected']}"
        )
        ui_elements_number.sequence_name.text.return_value = value["input"][
            "sequence_name"
        ]
        ui_elements_number.l_bound.value.return_value = value["input"]["l_bound"]
        ui_elements_number.u_bound.value.return_value = value["input"]["u_bound"]
        ui_elements_number.n_groups.value.return_value = value["input"]["n_groups"]
        ui_elements_number.n_elements.value.return_value = value["input"]["n_elements"]

        with pytest.raises(InvalidInputError, match=value["expected"]):
            controller.check_input_fields()


def test_update_ui_for_errors(ui_elements_number):
    controller = NumberSequenceController(ui_elements_number, output_window=None)

    error = InvalidInputError("Sequence name cannot be empty")
    controller.update_ui_for_errors(error)
    assert ui_elements_number.sequence_name.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.sequence_name.setToolTip.called_with(str(error))

    error = InvalidInputError("Lower bound must be less than the upper bound")
    controller.update_ui_for_errors(error)
    assert ui_elements_number.l_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.l_bound.setToolTip.called_with(str(error))

    error = InvalidInputError("Upper bound must be greater than 0")
    controller.update_ui_for_errors(error)
    assert ui_elements_number.u_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.u_bound.setToolTip.called_with(str(error))

    error = InvalidInputError("Number of groups must be greater than 0")
    controller.update_ui_for_errors(error)
    assert ui_elements_number.n_groups.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.n_groups.setToolTip.called_with(str(error))

    error = InvalidInputError("Number of elements must be greater than 0")
    controller.update_ui_for_errors(error)
    assert ui_elements_number.n_elements.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.n_elements.setToolTip.called_with(str(error))

    error = InvalidInputError(
        "The range of numbers must be greater than the number of elements"
    )
    controller.update_ui_for_errors(error)
    assert ui_elements_number.l_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.l_bound.setToolTip.called_with(str(error))
    assert ui_elements_number.u_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
    assert ui_elements_number.u_bound.setToolTip.called_with(str(error))

    error = InvalidInputError("Sequence generation failed")
    controller.update_ui_for_errors(error)
    assert ui_elements_number.l_bound.setStyleSheet.called_with(
        "color: red; border: 1px solid red;"
    )
