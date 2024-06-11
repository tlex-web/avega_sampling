import pytest
import pytest_mock
from library.custom_errors.InvalidInputError import InvalidInputError


mocker = pytest_mock.mocker


def test_invalid_input_error(mocker):
    mocker.patch("library.custom_errors.InvalidInputError.__init__", return_value=None)
    error = InvalidInputError("test message")
    assert str(error) == "test message"
    assert isinstance(error, Exception)
    assert isinstance(error, InvalidInputError)
