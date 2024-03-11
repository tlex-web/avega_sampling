from PyQt6.QtGui import QAction


class MenuController:
    def __init__(
        self,
        btn_action_save: QAction,
        btn_action_save_as: QAction,
        btn_action_about: QAction,
        btn_action_how_to: QAction,
        about_window,
        help_window,
    ) -> None:
        self.btn_action_save = btn_action_save
        self.btn_action_save_as = btn_action_save_as
        self.btn_action_about = btn_action_about
        self.btn_action_how_to = btn_action_how_to
        self.about_window = about_window
        self.help_window = help_window

        # Setup signals and slots for number sequence-related actions
        btn_action_save.triggered.connect(self.save)
        btn_action_save_as.triggered.connect(self.save_as)
        btn_action_about.triggered.connect(self.about)
        btn_action_how_to.triggered.connect(self.how_to)

    def save(self):
        """
        Saves the current file.
        """
        print("Save")

    def save_as(self):
        """
        Saves the current file with a new name.
        """
        print("Save as")

    def about(self):
        """
        Opens the about window.
        """
        if not self.about_window.isVisible():
            self.about_window.show()

    def how_to(self):
        """
        Opens the how to window.
        """
        if not self.help_window.isVisible():
            self.help_window.show()
