from datetime import date, datetime, timedelta


class PCGRNG:
    def __init__(self, initstate=0x853C49E6748FEA9B, initseq=0xDA3E39CB94B95BDB):
        """PCG Random Number Generator

        Args:
            initstate (hexadecimal, integer, optional): Initial state or given seed value. Defaults to 0x853C49E6748FEA9B.
            initseq (hexadecimal, optional): Initial sequential value. Defaults to 0xDA3E39CB94B95BDB.
        """
        self.state = 0
        self.inc = (initseq << 1) | 1
        self.max = 0xFFFFFFFFFFFFFFFF
        self.seed(initstate)

    def seed(self, seed_value: int):
        """Seed the random number generator

        Args:
            seed_value (int): The seed value
        """
        self.state = 0
        self.step()
        self.state += seed_value
        self.step()

    def step(self):
        self.state = (self.state * 6364136223846793005 + self.inc) & self.max

    def next(self):
        self.step()
        xorshifted = (((self.state >> 18) ^ self.state) >> 27) & self.max
        rot = self.state >> 59
        return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF

    def get_random_number(self, min_val: int, max_val: int):
        """Generates a random number in the given range

        Args:
            min_val (int): The minimum value of the range (inclusive)
            max_val (int): The maximum value of the range (inclusive)

        Returns:
            int: A random number within the specified range
        """
        range_size = max_val - min_val + 1
        return min_val + self.next() % range_size

    def get_unique_random_number_sequence(
        self, min_val: int, max_val: int, length: int
    ):
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
        if length > (max_val - min_val + 1):
            raise ValueError(
                f"Length of sequence exceeds the number of unique values in the range: {min_val} to {max_val} (inclusive) with length {length}"
            )

        sequence = set()
        while len(sequence) < length:
            number = self.get_random_number(min_val, max_val)
            sequence.add(number)

        return list(sequence)

    def get_random_date(self, start_date, end_date):
        """
        Generates a random date within a given start and end date.

        Parameters:
        - start_date (datetime): The start date.
        - end_date (datetime): The end date.

        Returns:
        - datetime: A random date within the specified range.
        """
        delta = end_date - start_date
        random_day = self.get_random_number(0, delta.days)
        return start_date + timedelta(days=random_day)

    def create_unique_date_sequence(
        self, start_date: date, end_date: date, length: int, order
    ):
        """
        Creates a unique sequence of random dates within a specified start and end date range.

        Parameters:
        - start_date (str): The start date in "YYYY-MM-DD" format.
        - end_date (str): The end date in "YYYY-MM-DD" format.
        - length (int): The number of unique dates to generate.

        Returns:
        - list[datetime]: An array of unique random dates within the specified range.
        """

        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

        if (end_date_dt - start_date_dt).days < length:
            raise ValueError(
                "The range between start and end date is not enough to generate the requested number of unique dates."
            )

        unique_dates = set()
        while len(unique_dates) < length:
            random_date = self.get_random_date(start_date_dt, end_date_dt)
            unique_dates.add(random_date)

        if order == "ascending":
            return sorted(list(unique_dates))
        elif order == "descending":
            return sorted(list(unique_dates), reverse=True)
        else:
            return list(unique_dates)
