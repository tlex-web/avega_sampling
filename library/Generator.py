from abc import ABC, abstractmethod

from library.PRNG.PCGRNG import PCGRNG


class Generator(ABC):

    def __init__(self):
        self.rng = PCGRNG()
        self.seed = None

    def set_seed(self, seed: int | None = None):
        """Set the seed for the random number generator (Optional)

        Args:
            seed (int): Seed value as integer with a maximum value of 2^32

        Raises:
            ValueError: If the seed value is not an integer or None
        """

        if not isinstance(seed, int | type(None)):
            raise ValueError("Seed value must be an integer or None")

        if seed is None:
            seed = self.rng.get_random_number(1, 2**32 - 1)

        self.seed = seed
        self.rng.seed(seed)

    @abstractmethod
    def generate_and_return_sequence(self):
        pass
