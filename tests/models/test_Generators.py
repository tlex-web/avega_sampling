import pytest
from datetime import date

from models.Generators import RandomDatesSequenceGenerator


@pytest.fixture
def generator():
    return RandomDatesSequenceGenerator()


def test_generate_and_return_sequence(generator):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    length = 5

    sequence = generator.generate_and_return_sequence(start_date, end_date, length)

    assert len(sequence) == length
    assert all(start_date <= date <= end_date for date in sequence)


def test_generate_and_return_sequence_exclude_saturdays(generator):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    length = 5

    sequence = generator.generate_and_return_sequence(
        start_date, end_date, length, exclude_saturdays=True
    )

    assert len(sequence) == length
    assert all(
        start_date <= date <= end_date and date.weekday() != 5 for date in sequence
    )


def test_generate_and_return_sequence_exclude_sundays(generator):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    length = 5

    sequence = generator.generate_and_return_sequence(
        start_date, end_date, length, exclude_sundays=True
    )

    assert len(sequence) == length
    assert all(
        start_date <= date <= end_date and date.weekday() != 6 for date in sequence
    )


def test_generate_and_return_sequence_exclude_holidays(generator):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    length = 5
    holidays = [date(2022, 1, 1), date(2022, 1, 15)]

    sequence = generator.generate_and_return_sequence(
        start_date, end_date, length, holidays=holidays
    )

    assert len(sequence) == length
    assert all(
        start_date <= date <= end_date and date not in holidays for date in sequence
    )


def test_generate_and_return_sequence_length_exceeds_unique_dates(generator):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    length = 40

    with pytest.raises(ValueError):
        generator.generate_and_return_sequence(start_date, end_date, length)
