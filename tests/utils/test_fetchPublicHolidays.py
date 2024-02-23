import pytest
from unittest.mock import patch
from utils.FetchPublicHolidays import FetchPublicHolidays
from requests.exceptions import HTTPError

from tests.fixtures import fetch_public_holidays


def test_validate_year_valid():
    year = 2022
    fetch_public_holidays = FetchPublicHolidays(year)
    assert fetch_public_holidays.year == year


def test_validate_year_invalid():
    with pytest.raises(ValueError):
        FetchPublicHolidays("2022")  # type: ignore


def test_get_public_holidays(fetch_public_holidays):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = (
            '[{"date": "2022-01-01", "name": "New Year\'s Day"}]'
        )
        holidays = fetch_public_holidays.get_public_holidays()
        assert len(holidays) == 1
        assert holidays[0]["date"] == "2022/01/01"
        assert holidays[0]["name"] == "New Year's Day"


def test_get_public_holidays_http_error(fetch_public_holidays):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = HTTPError
        with pytest.raises(SystemExit):
            fetch_public_holidays.get_public_holidays()
