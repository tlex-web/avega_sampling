import requests
import json

from utils.Logger import Logger

log = Logger()


class FetchPublicHolidays:
    def __init__(self, year: int):
        """Fetch dates of public holidays in Luxembourg for a given year and return them as a list

        Args:
            year (int): _description_
        """
        self.year = self.validate_year(year)

    def validate_year(self, year: int):
        """Validate the year

        Raises:
            ValueError: _description_
        """

        if year and isinstance(year, int):
            if year < 2000 or year > 2100:
                raise ValueError("Year must be between 2000 and 2100.")
            else:
                return year
        else:
            raise ValueError("Year must be an integer.")

    def get_public_holidays(self):
        """Fetch the public holidays from the API and reformat the dates

        Returns:
            list[dict]: List of public holidays
        """
        try:
            response = requests.get(
                f"https://date.nager.at/api/v2/publicholidays/{self.year}/LU"
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            log.error(e)
            raise SystemExit(e)

        holidays = json.loads(response.text)
        for holiday in holidays:
            holiday["date"] = holiday["date"].replace("-", "/")

        log.info(f"Public holidays for {self.year} fetched successfully.")

        return holidays
