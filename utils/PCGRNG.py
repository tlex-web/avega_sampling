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
            min_val (int): _description_
            max_val (int): _description_

        Returns:
            int
        """
        range_size = max_val - min_val + 1
        return min_val + self.next() % range_size

    def get_unique_random_sequence(self, min_val: int, max_val: int, length: int):
        """Generates a sequence of unique random numbers

        Args:
            min_val (int): _description_
            max_val (int): _description_
            length (int): _description_

        Raises:
            ValueError

        Returns:
            list[int]
        """
        if length > (max_val - min_val + 1):
            raise ValueError(
                "Length of sequence exceeds the number of unique values in the range."
            )

        sequence = set()
        while len(sequence) < length:
            number = self.get_random_number(min_val, max_val)
            sequence.add(number)

        return list(sequence)