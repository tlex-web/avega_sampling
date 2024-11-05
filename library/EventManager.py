from PyQt6.QtCore import QObject, pyqtSignal


class EventManager(QObject):
    # Define signals
    seed_set = pyqtSignal(int)  # Emitted when a seed is set
    request_seed = pyqtSignal()  # Emitted when a seed is required
    sequence_generated = pyqtSignal(list)  # Emitted when a sequence is generated
