from PyQt6.QtWidgets import QPushButton
from utils.PCGRNG import PCGRNG
from app import SeedWindow


class SeedController:
    def __init__(
        self,
        seed_window: SeedWindow,
    ) -> None:
        """
        Initializes the seed controller.
        """
        self.seed_window = seed_window
        self.pcgrng = PCGRNG()
