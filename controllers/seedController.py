from PyQt6.QtWidgets import QPushButton, QDialog
from utils.PCGRNG import PCGRNG


class SeedController:
    def __init__(self, btn_seed: QPushButton, seed_window: QDialog) -> None:
        self.btn_seed = btn_seed
        self.seed_window = seed_window

        # Setup signals and slots for seed-related actions
        self.btn_seed.clicked.connect(self.generate_seed)

    def generate_seed(self):
        """Generates a seed for the number sequence."""
        seed = PCGRNG().generate_seed()
        self.seed_window.seed_element.setText(str(seed))
        self.seed_window.show()
