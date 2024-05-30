from abc import ABC, abstractmethod

from models.Seed import Seed
from models.User import User
from config import SESSION_NAME


class BaseSequenceController(ABC):

    def __init__(self, generator):
        self.seed_model = Seed()
        self.user_model = User()
        self.generator = generator

    def check_session(self):
        # 1) Check if the user has set a seed
        # 2) If not, generate a seed
        # 3) If yes, use the user's seed
        # 4) Set the seed for the random number generator
        user_dict = self.user_model.read_user_username(SESSION_NAME)

        if user_dict is not None:
            user_id = user_dict["user_id"]

        seed = self.seed_model.read_seed(user_id)

        if seed is not None:
            seed_value = int(seed["seed_value"])
        else:
            seed_value = None

        self.generator.set_seed(seed_value)

    @abstractmethod
    def clear_fields(self):
        pass

    @abstractmethod
    def check_input_fields(self):
        pass

    @abstractmethod
    def generate_sequence(self):
        pass

    @abstractmethod
    def handle_generate_sequence_btn(self):
        pass
