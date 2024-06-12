from typing import NamedTuple
from PyQt6.QtCore import QObject, pyqtSignal
from string import Template

from library.Logger import log, LogEnvironment


class Output(NamedTuple):
    lower_bound: float
    upper_bound: float
    optional_params: dict
    n_groups: int
    n_elements: int
    seed: int
    output: dict


class PrintOutputSignals(QObject):
    send_output = pyqtSignal(str)


class PrintOutput:
    def __init__(
        self,
    ) -> None:
        self.signals = PrintOutputSignals()
        self.output = None

    def set_output(self, output: Output) -> None:
        """Set the output to be printed.

        Args:
            output (Output): The output to be printed.
        """

        if isinstance(output, Output):
            self.output = output
        else:
            log.error(
                "The output must be an instance of the Output class.",
                LogEnvironment.UTILS,
            )
            raise TypeError("The output must be an instance of the Output class.")

    def output_to_template_str(self):
        """Generate a HTML report based on the generated output.

        Returns:
            str: A string containing the generated HTML report.
        """

        try:
            with open("view/templates/output_window.html", "r") as file:
                template = Template(file.read())

            if self.output:
                output = template.substitute(
                    {
                        "l_bound": self.output.lower_bound,
                        "u_bound": self.output.upper_bound,
                        "optional_params": self.output.optional_params,
                        "n_groups": self.output.n_groups,
                        "n_elements": self.output.n_elements,
                        "seed": self.output.seed,
                        "output": self.output.output,
                    }
                )

                print("output", output, "state", self.signals.send_output.signal)
                self.signals.send_output.emit(output)
                print("emit", self.signals.send_output.signal)

        except FileNotFoundError:
            log.error("The output template file was not found.", LogEnvironment.UTILS)
            raise FileNotFoundError("The output template file was not found.")
