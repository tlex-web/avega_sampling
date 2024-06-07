import pytest
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
        assert isinstance(holiday, dict)
        assert "date" in holiday
        assert "name" in holiday
        assert "localName" in holiday
        assert "countryCode" in holiday
        assert "fixed" in holiday

    # Check if the returned holidays are not empty
    assert len(holidays) > 0

    # Check if the returned holidays are sorted by date
    dates = [holiday["date"] for holiday in holidays]
    assert dates == sorted(dates)


# Run the test function
test_public_holidays()
