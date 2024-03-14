from PyQt6.QtWidgets import QPushButton
from utils.PCGRNG import PCGRNG
from models.Seed import Seed

# from app import SeedWindow


class SeedController:
    def __init__(
        self,
        seed_window,
    ) -> None:
        """
        Initializes the seed controller.
        """
        self.seed_window = seed_window
        self.pcgrng = PCGRNG()
        self.seed_model = Seed()

        # Setup signals and slots for number seed-related actions
        self.seed_window.radio_continue_using_seed.toggled.connect(
            self.set_continue_using_old_seed
        )
        self.seed_window.radio_new_seed.toggled.connect(self.set_new_seed)
        self.seed_window.radio_gen_new_seed.toggled.connect(self.set_gen_new_seed)
        self.seed_window.radio_old_seed.toggled.connect(
            self.set_regenerate_using_old_seed
        )
        self.seed_window.buttonBox.accepted.connect(self.save_seed)
        self.seed_window.buttonBox.rejected.connect(self.seed_window.close)

    def check_input(self, input):
        """
        Checks if the input is valid.
        """
        if input.value() == 0:
            input.setStyleSheet("border: 1px solid red;")
            return False
        else:
            input.setStyleSheet("border: 1px solid green;")
            return True

    def set_continue_using_old_seed(self):
        """
        Sets the seed to the old seed.
        """
        if self.check_input(self.seed_window.old_seed_continue):
            self.pcgrng.seed(self.seed_window.old_seed_continue.value())

    def set_new_seed(self):
        """
        Sets the seed to a new seed.
        """
        if self.check_input(self.seed_window.seed_input):
            self.pcgrng.seed(self.seed_window.seed_input.value())

    def set_gen_new_seed(self):
        """
        Generates a new seed.
        """
        seed = self.pcgrng.get_random_number(0, 2**32 - 1)
        self.pcgrng.seed(seed)

    def set_regenerate_using_old_seed(self):
        """
        Sets the seed to a user-defined seed.
        """
        if self.check_input(self.seed_window.old_seed_regenerate):
            self.pcgrng.seed(self.seed_window.old_seed_regenerate.value())

    def save_seed(self):
        """
        Saves the seed to the seed model.
        """
        self.seed_model.create_seed("test", 1)
        self.seed_window.close()
