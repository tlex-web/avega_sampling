from models.User import User


class UserController:
    def __init__(self, view):
        self.view = view
        self.model = User()
        self.setup_signals()

    def setup_signals(self):
        # Assuming the view has buttons or actions for these operations
        self.view.add_user_signal.connect(self.add_user)
        self.view.update_user_signal.connect(self.update_user)
        self.view.delete_user_signal.connect(self.delete_user)

    def add_user(self, name):
        if self.model.create_user(name):
            self.view.show_message("User added successfully")
        else:
            self.view.show_error("Failed to add user")

    def update_user(self, user_id, name):
        if self.model.update_user(user_id, name):
            self.view.show_message("User updated successfully")
        else:
            self.view.show_error("Failed to update user")

    def delete_user(self, user_id):
        if self.model.delete_user(user_id):
            self.view.show_message("User deleted successfully")
        else:
            self.view.show_error("Failed to delete user")
