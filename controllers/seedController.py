from PyQt6.QtWidgets import QPushButton
from utils.PCGRNG import PCGRNG


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
