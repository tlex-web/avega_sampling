import unittest
import requests
from unittest.mock import patch
from datetime import date
from library.helpers.PublicHolidays import FetchPublicHolidays


class TestFetchPublicHolidays(unittest.TestCase):
    def setUp(self):
        self.fetch_holidays = FetchPublicHolidays()

    def test_set_period_valid_years(self):
        self.fetch_holidays.set_period(2022, 2023)
        self.assertEqual(self.fetch_holidays.start_year, 2022)
        self.assertEqual(self.fetch_holidays.end_year, 2023)

    def test_set_period_invalid_years(self):
        with self.assertRaises(ValueError):
            self.fetch_holidays.set_period(1999, 2101)

    @patch("utils.FetchPublicHolidays.requests.get")
    def test_get_public_holidays_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = '[{"date": "2022-01-01", "name": "New Year\'s Day", "localName": "New Year\'s Day", "countryCode": "LU", "fixed": true}]'

        self.fetch_holidays.set_period(2022, 2022)
        holidays = self.fetch_holidays.get_public_holidays()

        self.assertEqual(len(holidays), 1)
        self.assertEqual(holidays[0]["date"], "2022/01/01")
        self.assertEqual(holidays[0]["name"], "New Year's Day")

    @patch("utils.FetchPublicHolidays.requests.get")
    def test_get_public_holidays_http_error(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        self.fetch_holidays.set_period(2022, 2022)
        holidays = self.fetch_holidays.get_public_holidays()

        self.assertIsNone(holidays)

    @patch("utils.FetchPublicHolidays.requests.get")
    def test_get_public_holidays_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request exception")

        self.fetch_holidays.set_period(2022, 2022)
        holidays = self.fetch_holidays.get_public_holidays()

        self.assertIsNone(holidays)

    @patch("utils.FetchPublicHolidays.requests.get")
    def test_get_public_holidays_generic_exception(self, mock_get):
        mock_get.side_effect = Exception("Generic exception")

        self.fetch_holidays.set_period(2022, 2022)
        holidays = self.fetch_holidays.get_public_holidays()

        self.assertIsNone(holidays)

    def test_get_public_holidays_invalid_year_type(self):
        with self.assertRaises(ValueError):
            self.fetch_holidays.set_period("2022", "2023")

    def test_get_public_holidays_invalid_year_range(self):
        with self.assertRaises(ValueError):
            self.fetch_holidays.set_period(1999, 2101)

    def test_get_one_year_period(self):
        self.fetch_holidays.set_period(2022, 2022)
        holidays = self.fetch_holidays.get_public_holidays()

        self.assertIsNotNone(holidays)
        self.assertEqual(len(holidays), 12)

    def test_get_multiple_year_period(self):
        self.fetch_holidays.set_period(2022, 2023)
        holidays = self.fetch_holidays.get_public_holidays()

        self.assertIsNotNone(holidays)
        self.assertTrue(len(holidays) > 1)


if __name__ == "__main__":
    unittest.main()
