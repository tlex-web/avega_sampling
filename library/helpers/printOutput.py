from typing import NamedTuple
from string import Template

from library.Logger import log, LogEnvironment


class Output(NamedTuple):
    lower_bound: int | float | str
    upper_bound: int | float | str
    optional_params: dict
    n_groups: int
    n_elements: int
    seed: int | float
    output: dict


class PrintOutput:

    def __init__(
        self,
    ) -> None:
        self.output = None

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
                        "%l_bound%": self.output.lower_bound,
                        "u_bound": self.output.upper_bound,
                        "optional_params": self.output.optional_params,
                        "n_groups": self.output.n_groups,
                        "n_elements": self.output.n_elements,
                        "seed": self.output.seed,
                        "output": self.output.output,
                    }
                )

                return output

        except FileNotFoundError:
            log.error("The output template file was not found.", LogEnvironment.UTILS)
            raise FileNotFoundError("The output template file was not found.")
