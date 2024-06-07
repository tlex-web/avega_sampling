import requests
import json
from library.Logger import log, LogEnvironment


class PublicHolidays:
    def __init__(self):
        """Fetch dates of public holidays in Luxembourg for a given period and return them as a list"""
        self.start_year = None
        self.end_year = None

    def set_period(self, start_year: int, end_year: int):
        """Validate the start and end years

        Args:
            start_year (int): The start year to validate
            end_year (int): The end year to validate

        Raises:
            ValueError: If the years are not valid integers or are outside the range of 2000 to 2100
        """
        if (
            start_year
            and isinstance(start_year, int)
            and end_year
            and isinstance(end_year, int)
        ):
            if (
                start_year < 2000
                or start_year > 2100
                or end_year < 2000
                or end_year > 2100
            ):
                raise ValueError("Years must be between 2000 and 2100.")
            else:
                self.start_year = start_year
                self.end_year = end_year
        else:
            raise ValueError("Years must be integers.")

    def return_list_public_holidays(self):
        """Fetch the public holidays from the API and reformat the dates

        Returns:
            list[dict]: List of public holidays, where each holiday is represented as a dictionary
                        with keys 'date', 'name', 'localName', 'countryCode', and 'fixed'
        """
        all_holidays = []
        if self.start_year is not None and self.end_year is not None:
            for year in range(self.start_year, self.end_year + 1):
                try:
                    response = requests.get(
                        f"https://date.nager.at/api/v3/publicholidays/{year}/LU"
                    )
                    response.raise_for_status()

                    holidays = json.loads(response.text)

                    all_holidays.extend(holidays)

                    holidays_dates = [holiday["date"] for holiday in holidays]

                    log.info(
                        f"Public holidays for {year} fetched successfully.",
                        LogEnvironment.UTILS,
                    )

                    return holidays_dates

                except requests.exceptions.HTTPError as e:
                    log.error(e, LogEnvironment.UTILS)
                    return None
                except requests.exceptions.RequestException as e:
                    log.error(e, LogEnvironment.UTILS)
                    return None
                except Exception as e:
                    log.error(e, LogEnvironment.UTILS)
                    return None
