from PyQt6.QtWidgets import QPushButton


class WindowController:
    def __init__(
        self,
        btn_new_file: QPushButton,
        btn_save_as: QPushButton,
        btn_save: QPushButton,
        btn_copy: QPushButton,
        btn_paste: QPushButton,
        btn_help: QPushButton,
        help_window,
    ) -> None:

        self.btn_new_file = btn_new_file
        self.btn_save_as = btn_save_as
        self.btn_save = btn_save
        self.btn_copy = btn_copy
        self.btn_paste = btn_paste
        self.btn_help = btn_help
        self.help_window = help_window

        # Setup signals and slots for number sequence-related actions
        btn_new_file.clicked.connect(self.new_file)
        btn_save_as.clicked.connect(self.save_as)
        btn_save.clicked.connect(self.save)
        btn_copy.clicked.connect(self.copy)
        btn_paste.clicked.connect(self.paste)
        btn_help.clicked.connect(self.help)

    def new_file(self):
        """
        Opens a new file.
        """
        print("New file")

    def save_as(self):
        """
        Saves the current file with a new name.
        """
        print("Save as")

    def save(self):
        """
        Saves the current file.
        """
        print("Save")

    def copy(self):
        """
        Copies the selected text.
        """
        print("Copy")

    def paste(self):
        """
        Pastes the copied text.
        """
        print("Paste")

    def help(self):
        """
        Shows or hides the help window based on its current visibility state.
        """
        if not self.help_window.isVisible():
            self.help_window.show()
        else:
            self.help_window.hide()
