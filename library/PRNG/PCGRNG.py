# Description: PCG Random Number Generator implementation in Python
#
# The PCG Random Number Generator is a family of simple fast space-efficient statistically good algorithms for random number generation. The PCG-XSH-RR variant is used in this implementation.
#
# The PCG-XSH-RR variant is a 64-bit generator with 32-bit output and a 128-bit state. It has a period of 2^64 and supports a seed value of 2^128.
#


class PCGRNG:

    def __init__(self, initstate=None, initseq=0xDA3E39CB94B95BDB):
        """PCG Random Number Generator

        Args:
            initstate (int, optional): Initial state or given seed value. If None, a default seed is used.
            initseq (int, optional): Initial sequential value. Defaults to 0xDA3E39CB94B95BDB.
        """
        self.state = 0
        self.inc = (initseq << 1) | 1
        self.max = 0xFFFFFFFFFFFFFFFF
        if initstate is not None:
            self.seed(initstate)
        else:
            self.step()  # Initialize with a step if no seed is provided

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
        range_size = max_val - min_val
        return min_val + self.next() % (range_size + 1)
