from models.Seed import Seed


class SeedController:
    def __init__(self, view):
        self.view = view
        self.model = Seed()
        # Assume the view has signals for these actions
        self.view.add_seed_signal.connect(self.add_seed)

    def add_seed(self, name, description):
        if self.model.create_seed(name, description):
            self.view.show_message("Seed added successfully")
        else:
            self.view.show_error("Failed to add seed")
