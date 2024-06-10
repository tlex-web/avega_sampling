from library.PRNG.PCGRNG import PCGRNG
from library.Generator import Generator
from library.custom_errors.InvalidInputError import InvalidInputError


class RandomNumberSequenceGenerator(Generator):

    def __init__(self):
        super().__init__()

        self.rng = PCGRNG()
        self.seed = None

    def generate_and_return_sequence(self, l_bound: int, u_bound: int, length: int):
        """Generates a sequence of unique random numbers

        Args:
            min_val (int): The minimum value of the range (inclusive)
            max_val (int): The maximum value of the range (inclusive)
            length (int): The length of the sequence

        Raises:
            InvalidInputError: If the length of the sequence exceeds the number of unique values in the range

        Returns:
            list[int]: A list of unique random numbers within the specified range
        """

        generated_numbers = set()
        counter = 0

        while len(generated_numbers) != length:
            random_number = self.rng.get_random_number(l_bound, u_bound)
            generated_numbers.add(random_number)
            counter += 1

            if counter > length:
                raise InvalidInputError(
                    "The length of the sequence exceeds the number of unique values in the range"
                )

        return list(generated_numbers)
