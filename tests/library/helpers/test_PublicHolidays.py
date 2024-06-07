import pytest
from datetime import datetime
from library.helpers.PublicHolidays import PublicHolidays


def test_public_holidays():
    # Create an instance of PublicHolidays
    ph = PublicHolidays()

    # Set the period for testing
    ph.set_period(2022, 2023)

    # Call the return_list_public_holidays method
    holidays = ph.return_list_public_holidays()

    # Check if the returned holidays are not None
    assert holidays is not None

    # Check if the returned holidays are of type list
    assert isinstance(holidays, list)

    # Check if the returned holidays contain dictionaries with the required keys
    for holiday in holidays:
        assert isinstance(holiday, str)

    # Check if the returned holidays are not empty
    assert len(holidays) > 0

    # Check if the returned holidays are sorted by date
    assert holidays == sorted(holidays)


def test_set_period():
    ph = PublicHolidays()

    # Test valid start and end years
    ph.set_period(2022, 2023)
    assert ph.start_year == 2022
    assert ph.end_year == 2023

    # Test invalid start year
    with pytest.raises(ValueError):
        ph.set_period(1999, 2023)

    # Test invalid end year
    with pytest.raises(ValueError):
        ph.set_period(2022, 2101)

    # Test invalid start and end years
    with pytest.raises(ValueError):
        ph.set_period(1999, 2101)

    # Test non-integer start year
    with pytest.raises(ValueError):
        ph.set_period("2022", 2023)  # type: ignore

    # Test non-integer end year
    with pytest.raises(ValueError):
        ph.set_period(2022, "2023")  # type: ignore

    # Test non-integer start and end years
    with pytest.raises(ValueError):
        ph.set_period("2022", "2023")  # type: ignore


def test_return_list_public_holidays():
    ph = PublicHolidays()

    # Test return_list_public_holidays without setting the period
    holidays = ph.return_list_public_holidays()
    assert holidays is None

    # Test return_list_public_holidays with valid period
    ph.set_period(2022, 2023)
    holidays = ph.return_list_public_holidays()
    assert isinstance(holidays, list)

    # Test return_list_public_holidays with invalid period
    with pytest.raises(Exception):
        ph.set_period(2100, 2101)
        holidays = ph.return_list_public_holidays()
        assert holidays is None


def test_returned_dates_valid_iso_format():
    ph = PublicHolidays()
    ph.set_period(2022, 2023)
    holidays = ph.return_list_public_holidays()
    for holiday in holidays if holidays is not None else []:
        assert holiday == datetime.strptime(holiday, "%Y-%m-%d").date().isoformat()
