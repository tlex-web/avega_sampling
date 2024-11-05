from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QObject

# from app import OutputWindow
from library.helpers.printOutput import PrintOutput


class OutputWindowController(QObject):
    def __init__(
        self,
        output_window,
        event_manager,
        btn_generate_numbers: QPushButton,
        btn_generate_dates: QPushButton,
        print_output: PrintOutput,
    ) -> None:
        super().__init__()
        self.output_window = output_window
        self.event_manager = event_manager
        self.btn_generate_numbers = btn_generate_numbers
        self.btn_generate_dates = btn_generate_dates
        self.print_output = print_output

        self.event_manager.sequence_generated.connect(self.show_output)
        self.output_window.pushButton_save_as_output.clicked.connect(self.save_output)

    def show_output(self, dto) -> None:
        """Show the output in the output window.

        Args:
            output (Output): The output to be displayed.
        """

        # reformat the output to be displayed in the output window

        self.current_dto = self.print_output.output_to_template_str()
        self.output_window.output_element.setHtml(self.current_dto)
        self.output_window.show()

    def save_output(self) -> None:
        """Save the output to a file.

        Args:
            output (Output): The output to be saved.
        """

        file_path, _ = QFileDialog.getSaveFileName(
            self.output_window, "Save Output", "", "HTML Files (*.html)"
        )

        if file_path and self.current_dto:
            with open(file_path, "w") as file:
                file.write(self.current_dto)
