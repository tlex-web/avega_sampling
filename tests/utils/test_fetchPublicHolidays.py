import pytest
from utils.FetchPublicHolidays import FetchPublicHolidays


@pytest.mark.parametrize("year", [2022, 2023, 2024])
def test_fetch_public_holidays_valid_year(year):
    fetcher = FetchPublicHolidays(year)
    holidays = fetcher.get_public_holidays()
    assert isinstance(holidays, list)
    assert all(isinstance(holiday, dict) for holiday in holidays)
    assert all("date" in holiday for holiday in holidays)
    assert all("name" in holiday for holiday in holidays)
    assert all("localName" in holiday for holiday in holidays)
    assert all("countryCode" in holiday for holiday in holidays)
    assert all("fixed" in holiday for holiday in holidays)


@pytest.mark.parametrize("year", [1999, 2101])
def test_fetch_public_holidays_invalid_year(year):
    with pytest.raises(ValueError):
        FetchPublicHolidays(year)


def test_fetch_public_holidays_api_failure(requests_mock):
    requests_mock.get(
        "https://date.nager.at/api/v3/publicholidays/2022/LU", status_code=500
    )
    fetcher = FetchPublicHolidays(2022)
    holidays = fetcher.get_public_holidays()
    assert holidays is None


def test_fetch_public_holidays_request_exception(requests_mock):
    requests_mock.get(
        "https://date.nager.at/api/v3/publicholidays/2022/LU",
        exc=requests.exceptions.RequestException,
    )
    fetcher = FetchPublicHolidays(2022)
    holidays = fetcher.get_public_holidays()
    assert holidays is None


def test_fetch_public_holidays_other_exception(requests_mock):
    requests_mock.get(
        "https://date.nager.at/api/v3/publicholidays/2022/LU", exc=Exception
    )
    fetcher = FetchPublicHolidays(2022)
    holidays = fetcher.get_public_holidays()
    assert holidays is None
