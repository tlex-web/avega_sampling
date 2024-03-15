import requests
import json


from utils.Logger import log, LogEnvironment


class FetchPublicHolidays:
    def __init__(self, year: int):
        """Fetch dates of public holidays in Luxembourg for a given year and return them as a list

        Args:
            year (int): The year for which to fetch the public holidays

        Raises:
            ValueError: If the year is not a valid integer or is outside the range of 2000 to 2100
        """
        self.year = self.validate_year(year)

    def validate_year(self, year: int):
        """Validate the year

        Args:
            year (int): The year to validate

        Returns:
            int: The validated year

        Raises:
            ValueError: If the year is not a valid integer or is outside the range of 2000 to 2100
        """
        if year and isinstance(year, int):
            if year < 2000 or year > 2100:
                raise ValueError("Year must be between 2000 and 2100.")
            else:
                return year
        else:
            raise ValueError("Year must be an integer.")

    async def get_public_holidays(self):
        """Fetch the public holidays from the API and reformat the dates

        Returns:
            list[dict]: List of public holidays, where each holiday is represented as a dictionary
                        with keys 'date', 'name', 'localName', 'countryCode', and 'fixed'
        """

        try:
            response = requests.get(
                f"https://date.nager.at/api/v3/publicholidays/{self.year}/LU"
            )
            response.raise_for_status()

            holidays = json.loads(response.text)
            for holiday in holidays:
                holiday["date"] = holiday["date"].replace("-", "/")

            log.info(
                f"Public holidays for {self.year} fetched successfully.",
                LogEnvironment.UTILS,
            )
            return holidays

        except requests.exceptions.HTTPError as e:
            log.error(e, LogEnvironment.UTILS)
            return None
        except requests.exceptions.RequestException as e:
            log.error(e, LogEnvironment.UTILS)
            return None
        except Exception as e:
            log.error(e, LogEnvironment.UTILS)
            return None
