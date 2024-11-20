from PyQt6.QtCore import QObject, pyqtSignal

from library.helpers.printOutput import Output


class EventManager(QObject):
    # Define signals
    seed_set = pyqtSignal(int)  # Emitted when a seed is set
    open_seed_window = pyqtSignal()  # Emitted when the seed window should be opened
    request_seed = pyqtSignal()  # Emitted when a seed is required
    sequence_generated = pyqtSignal(Output)  # Emitted when a sequence is generated
