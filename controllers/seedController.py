# from app import SeedWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QObject

from library.PRNG.PCGRNG import PCGRNG
from models.Seed import Seed
from models.User import User
from library.Logger import log, LogEnvironment


class SeedController(QObject):
    def __init__(
        self,
        seed_window,
        event_manager,
        btn_set_seed_numbers: QPushButton,
        btn_set_seed_dates: QPushButton,
    ) -> None:
        """
        Initializes the seed controller.
        """
        super().__init__()
        self.seed_window = seed_window
        self.event_manager = event_manager
        self.btn_set_seed_numbers = btn_set_seed_numbers
        self.btn_set_seed_dates = btn_set_seed_dates
        self.seed_model = Seed()
        self.pcgrng = PCGRNG()
        self.user_model = User()
        self.seed = None

        # Setup signals and slots for number seed-related actions
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

    def save_seed(self):
        """
        Saves the seed to the seed model.
        """
        if self.seed_window.radio_gen_new_seed.isChecked():
            self.check_input(self.seed_window.seed_input)
            self.seed = self.pcgrng.get_random_number(
                1, 2**32 - 1
            )  # 2**32 - 1 is the maximum value for a 32-bit integer
        elif self.seed_window.radio_new_seed.isChecked():
            self.check_input(self.seed_window.seed_input)
            self.seed = self.seed_window.seed_input.value()
        elif self.seed_window.radio_old_seed.isChecked():
            self.check_input(self.seed_window.old_seed_continue)
            self.seed = self.seed_window.old_seed_continue.value()
        elif self.seed_window.radio_continue_using_seed.isChecked():
            self.check_input(self.seed_window.old_seed_regenerate)
            self.seed = self.seed_window.old_seed_regenerate.value()
        else:
            log.error("Failed to save seed", LogEnvironment.CONTROLLERS)

        self.event_manager.seed_set.emit(self.seed)
        self.seed_window.close()
