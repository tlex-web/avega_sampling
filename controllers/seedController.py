from models.Seed import Seed


class SeedController:
    def __init__(self, view):
        self.view = view
        self.model = Seed()

    def add_seed(self, name, description):
        if self.model.create_seed(name, description):
            self.view.show_message("Seed added successfully")
        else:
            self.view.show_error("Failed to add seed")
