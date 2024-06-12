from PyQt6.QtWidgets import QFileDialog


class OutputWindowController:
    def __init__(self, output_window, signals) -> None:
        self.output_window = output_window
        self.signals = signals
        self.current_dto = None

        self.output_window.pushButton_save_as_output.clicked.connect(self.save_output)
        self.signals.send_output.connect(self.show_output)
        print("connect", self.signals.send_output.signal)

    def show_output(self, dto) -> None:
        """Show the output in the output window.

        Args:
            output (Output): The output to be displayed.
        """
        self.current_dto = dto
        print("show_output", dto)

        if not self.output_window.isVisible():
            self.output_window.show()
            self.output_window.output_element.setHtml(dto)
        else:
            self.output_window.output_element.setHtml(dto)

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
