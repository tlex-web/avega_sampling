import pytest
from datetime import date
from models.RandomDatesSequenceGenerator import RandomDatesSequenceGenerator


@pytest.fixture
def generator():
    return RandomDatesSequenceGenerator()


def test_generate_random_date(generator):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 31)
    random_date = generator.generate_random_date(start_date, end_date)
    assert start_date <= random_date <= end_date


def test_generate_and_return_sequence(generator):
    l_bound = date(2022, 1, 1)
    u_bound = date(2022, 1, 31)
    length = 10
    sequence = generator.generate_and_return_sequence(l_bound, u_bound, length)
    assert len(sequence) == length
    for element in sequence:
        assert l_bound <= element <= u_bound


def test_generate_and_return_sequence_exclude_saturdays(generator):
    l_bound = date(2022, 1, 1)
    u_bound = date(2022, 1, 31)
    length = 10
    sequence = generator.generate_and_return_sequence(
        l_bound, u_bound, length, exclude_saturdays=True
    )
    assert len(sequence) == length
    for element in sequence:
        assert l_bound <= element <= u_bound
        assert element.weekday() != 5


def test_generate_and_return_sequence_exclude_sundays(generator):
    l_bound = date(2022, 1, 1)
    u_bound = date(2022, 1, 31)
    length = 10
    sequence = generator.generate_and_return_sequence(
        l_bound, u_bound, length, exclude_sundays=True
    )
    assert len(sequence) == length
    for element in sequence:
        assert l_bound <= element <= u_bound
        assert element.weekday() != 6


def test_generate_and_return_sequence_exclude_holidays(generator):
    l_bound = date(2022, 1, 1)
    u_bound = date(2022, 1, 12)
    length = 8
    holidays = [date(2022, 1, 1), date(2022, 1, 2)]
    sequence = generator.generate_and_return_sequence(
        l_bound, u_bound, length, holidays=holidays
    )
    assert len(sequence) == length
    for element in sequence:
        assert l_bound <= element <= u_bound
        assert element not in holidays


def test_generate_and_return_sequence_invalid_input(generator):
    l_bound = date(2022, 1, 1)
    u_bound = date(2022, 1, 31)
    length = 100
    with pytest.raises(Exception):
        generator.generate_and_return_sequence(l_bound, u_bound, length)


def test_generate_and_return_sequence_only_holidays_fail(generator):
    l_bound = date(2022, 1, 1)
    u_bound = date(2022, 1, 12)
    length = 8
    holidays = [
        date(2022, 1, 1),
        date(2022, 1, 2),
        date(2022, 1, 3),
        date(2022, 1, 4),
        date(2022, 1, 5),
        date(2022, 1, 6),
        date(2022, 1, 7),
        date(2022, 1, 8),
        date(2022, 1, 9),
        date(2022, 1, 10),
        date(2022, 1, 11),
        date(2022, 1, 12),
    ]
    with pytest.raises(Exception):
        generator.generate_and_return_sequence(
            l_bound, u_bound, length, holidays=holidays
        )
