from typing import NamedTuple
from string import Template

from library.Logger import log, LogEnvironment


class Output(NamedTuple):
    company_name: str | None
    year: int | None
    date: str
    sampling_method: str
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
                        "company_name": str(data.company_name),
                        "year": str(data.year),
                        "date": str(data.date),
                        "sampling_method": str(data.sampling_method),
                        "l_bound": str(data.lower_bound),
                        "u_bound": str(data.upper_bound),
                        "optional_params": str(data.optional_params),
                        "n_groups": str(data.n_groups),
                        "n_elements": str(data.n_elements),
                        "seed": str(data.seed),
                        "output": str(data.output),
                    }
                )

                return output

        except FileNotFoundError:
            log.error("The output template file was not found.", LogEnvironment.UTILS)
            return ""
        except Exception as e:
            log.error(f"Failed to generate output template: {e}", LogEnvironment.UTILS)
            return ""
