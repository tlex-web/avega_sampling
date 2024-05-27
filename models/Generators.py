from abc import ABC, abstractmethod
from datetime import date, timedelta
from PyQt6.QtCore import pyqtSignal

from utils.PCGRNG import PCGRNG


class Generator(ABC):

    @abstractmethod
    def set_seed(self, seed: int):
        pass

    @abstractmethod
    def generate_and_return_sequence(self):
        pass


class RandomNumberSequenceGenerator(Generator):
    error_rng_generation = pyqtSignal(str, name="error_rng_generation")

    def __init__(self):

        self.rng = PCGRNG()
        self.seed = None

    def set_seed(self, seed: int):
        """Set the seed for the random number generator (Optional)

        Args:
            seed (int): Seed value as integer with a maximum value of 2^128
        """
        self.seed = seed
        self.rng.seed(seed)

    def generate_and_return_sequence(self, l_bound: int, u_bound: int, length: int):
        """Generates a sequence of unique random numbers

        Args:
            min_val (int): The minimum value of the range (inclusive)
            max_val (int): The maximum value of the range (inclusive)
            length (int): The length of the sequence

        Raises:
            ValueError: If the length of the sequence exceeds the number of unique values in the range

        Returns:
            list[int]: A list of unique random numbers within the specified range
        """

        try:
            generated_numbers = set()

            while len(generated_numbers) < length:
                random_number = self.rng.get_random_number(l_bound, u_bound)
                generated_numbers.add(random_number)

            return list(generated_numbers)

        except Exception as e:
            self.error_rng_generation.emit(str(e))
            return []


class RandomDatesSequenceGenerator(Generator):
    error_rdg_generation = pyqtSignal(str, name="error_rdg_generation")

    def __init__(self):

        self.rng = PCGRNG()
        self.seed = None

    def set_seed(self, seed: int):
        """Set the seed for the random number generator (Optional)

        Args:
            seed (int): Seed value as integer with a maximum value of 2^128
        """
        self.seed = seed
        self.rng.seed(seed)

    def generate_random_date(self, start_date: date, end_date: date):
        """
        Generates a random date within a given start and end date.

        Parameters:
        - start_date (datetime): The start date.
        - end_date (datetime): The end date.

        Returns:
        - datetime: A random date within the specified range.
        """
        delta = end_date - start_date
        random_day = self.rng.get_random_number(0, delta.days)
        return start_date + timedelta(days=random_day)

    def generate_and_return_sequence(
        self,
        l_bound: date,
        u_bound: date,
        length: int,
        holidays: list[date] | None = None,
        exclude_saturdays: bool = False,
        exclude_sundays: bool = False,
    ) -> list[date]:
        """Generates a sequence of unique random dates

        Args:
            start_date (str): The start date in "YYYY-MM-DD" format
            end_date (str): The end date in "YYYY-MM-DD" format
            length (int): The length of the sequence
            holidays (list[datetime], optional): A list of dates to exclude from the sequence. Defaults to [].
            exclude_saturdays (bool, optional): Whether to exclude Saturdays from the sequence. Defaults to False.
            exclude_sundays (bool, optional): Whether to exclude Sundays from the sequence. Defaults to False.

        Raises:
            ValueError: If the length of the sequence exceeds the number of unique dates in the range

        Returns:
            list[datetime]: A list of unique random dates within the specified range
        """

        try:
            holidays_set = set(holidays)
            generated_dates = set()

            while len(generated_dates) < length:
                random_date = self.generate_random_date(l_bound, u_bound)

                if exclude_saturdays and random_date.weekday() == 5:
                    continue
                if exclude_sundays and random_date.weekday() == 6:
                    continue
                if random_date in holidays_set:
                    continue

                generated_dates.add(random_date)

            return list(generated_dates)

        except Exception as e:
            self.error_rdg_generation.emit(str(e))
            return []
