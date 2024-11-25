from abc import ABC, abstractmethod

from models.Seed import Seed
from models.User import User
from models.Session import Session

from config import SESSION_NAME


class BaseSequenceController(ABC):

    def __init__(self, generator):
        self.seed_model = Seed()
        self.user_model = User()
        self.session_model = Session()
        self.generator = generator

    def read_session(self):
        user_data = self.user_model.read_user_username(SESSION_NAME)

        if user_data is not None:
            user_id = user_data["user_id"]

            session = self.session_model.get_session(user_id)

            if session is not None:
                return session

        return None

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
    def generate_and_emit_sequence(self):
        pass
