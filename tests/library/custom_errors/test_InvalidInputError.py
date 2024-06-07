import pytest
from library.custom_errors.InvalidInputError import InvalidInputError


def test_invalid_input_error():
    message = "Invalid input"
    error = InvalidInputError(message)
    assert str(error) == message
    assert isinstance(error, Exception)
