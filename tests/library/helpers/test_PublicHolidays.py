import pytest
from datetime import date

from library.helpers.PublicHolidays import PublicHolidays

from fixtures import public_holidays


def test_public_holidays(public_holidays):

    public_holidays.set_period(2022, 2023)

    holidays = public_holidays.return_list_public_holidays()

    assert holidays is not None
    assert isinstance(holidays, list)

    for holiday in holidays:
        assert isinstance(holiday, date)

    assert len(holidays) > 0
    assert holidays == sorted(holidays)


def test_set_period(public_holidays):

    # Test valid start and end years
    public_holidays.set_period(2022, 2023)
    assert public_holidays.start_year == 2022
    assert public_holidays.end_year == 2023

    # Test invalid start year
    with pytest.raises(ValueError):
        public_holidays.set_period(1999, 2023)

    # Test invalid end year
    with pytest.raises(ValueError):
        public_holidays.set_period(2022, 2101)

    # Test invalid start and end years
    with pytest.raises(ValueError):
        public_holidays.set_period(1999, 2101)

    # Test non-integer start year
    with pytest.raises(ValueError):
        public_holidays.set_period("2022", 2023)  # type: ignore

    # Test non-integer end year
    with pytest.raises(ValueError):
        public_holidays.set_period(2022, "2023")  # type: ignore

    # Test non-integer start and end years
    with pytest.raises(ValueError):
        public_holidays.set_period("2022", "2023")  # type: ignore


def test_return_list_public_holidays(public_holidays):

    # Test return_list_public_holidays without setting the period
    holidays = public_holidays.return_list_public_holidays()
    assert holidays is None

    # Test return_list_public_holidays with valid period
    public_holidays.set_period(2022, 2023)
    holidays = public_holidays.return_list_public_holidays()
    assert isinstance(holidays, list)

    # Test return_list_public_holidays with invalid period
    with pytest.raises(Exception):
        public_holidays.set_period(2100, 2101)
        holidays = public_holidays.return_list_public_holidays()
        assert holidays is None


def test_returned_dates_valid_iso_format(public_holidays):

    public_holidays.set_period(2022, 2023)
    holidays = public_holidays.return_list_public_holidays()
    for holiday in holidays if holidays is not None else []:
        assert holiday.strftime("%Y-%m-%d") == holiday.isoformat()


def test_set_period_invalid_years(public_holidays):
    # Test invalid start year
    with pytest.raises(ValueError):
        public_holidays.set_period(1999, 2023)

    # Test invalid end year
    with pytest.raises(ValueError):
        public_holidays.set_period(2022, 2101)

    # Test invalid start and end years
    with pytest.raises(ValueError):
        public_holidays.set_period(1999, 2101)


def test_set_period_non_integer_years(public_holidays):
    # Test non-integer start year
    with pytest.raises(ValueError):
        public_holidays.set_period("2022", 2023)

    # Test non-integer end year
    with pytest.raises(ValueError):
        public_holidays.set_period(2022, "2023")

    # Test non-integer start and end years
    with pytest.raises(ValueError):
        public_holidays.set_period("2022", "2023")


def test_return_list_public_holidays_without_period(public_holidays):
    # Test return_list_public_holidays without setting the period
    holidays = public_holidays.return_list_public_holidays()
    assert holidays is None


def test_return_list_public_holidays_valid_period(public_holidays):
    # Test return_list_public_holidays with valid period
    public_holidays.set_period(2022, 2023)
    holidays = public_holidays.return_list_public_holidays()
    assert isinstance(holidays, list)


def test_return_list_public_holidays_invalid_period(public_holidays):
    # Test return_list_public_holidays with invalid period
    with pytest.raises(Exception):
        public_holidays.set_period(2100, 2101)
        holidays = public_holidays.return_list_public_holidays()
        assert holidays is None
