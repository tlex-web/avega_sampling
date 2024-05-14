from abc import ABC, abstractmethod


class BaseSequenceController(ABC):

    def __init__(self, view, models, pcgrng, *args, **kwargs):
        self.view = view
        self.models = models
        self.pcgrng = pcgrng

    @abstractmethod
    def check_session(self):
        pass

    @abstractmethod
    def clear_numbers(self):
        pass

    @abstractmethod
    def generate_sequence(self):
        pass

    @abstractmethod
    def sort_sequence(self):
        pass

    @abstractmethod
    def group_sequence(self):
        pass

    @abstractmethod
    def print_sequence(self):
        pass
