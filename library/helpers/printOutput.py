from typing import NamedTuple
from string import Template

from library.Logger import log, LogEnvironment


class Output(NamedTuple):
    lower_bound: int | str
    upper_bound: int | str
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

    def output_to_template_str(self, data: Output) -> str:
        """Generate a HTML report based on the generated output.

        Returns:
            str: A string containing the generated HTML report.
        """

        try:
            with open("view/templates/output_window.html", "r") as file:
                template = Template(file.read())

            if data:
                output = template.substitute(
                    {
                        "l_bound": data.lower_bound,
                        "u_bound": data.upper_bound,
                        "optional_params": data.optional_params,
                        "n_groups": data.n_groups,
                        "n_elements": data.n_elements,
                        "seed": data.seed,
                        "output": data.output,
                    }
                )

                return output

        except FileNotFoundError:
            log.error("The output template file was not found.", LogEnvironment.UTILS)
            raise FileNotFoundError("The output template file was not found.")
