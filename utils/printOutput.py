from PyQt6.QtWidgets import QTextEdit
from app import OutputWindow


class PrintOutput:
    def __init__(
        self,
        output_window: OutputWindow,
        company_name: str,
        company_year: str,
        output,
    ) -> None:
        self.output_window = output_window
        self.company_name = company_name
        self.company_year = company_year
        self.output = output

    def output_to_html(self) -> str:
        """Generate a HTML report based on the generated output.

        Returns:
            str: A string containing the generated HTML report.
        """
        for i, group in enumerate(self.output):
            self.output_window.output_element.append(f"Group {i+1}:")
            self.output_window.output_element.append(str(group))
            self.output_window.output_element.append("")
        return f"""
        <html>
        <head>
        <style>
        table {{
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }}

        td, th {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }}

        tr:nth-child(even) {{
            background-color: #dddddd;
        }}

        h1 {{
            text-align: center;
        }}
        </style>
        </head>
        <body>
        <h1>{self.company_name} - {self.company_year}</h1>
        <table>
            <tr>
                <th>Output</th>
            </tr>
            <tr>
                <td>{self.output}</td>
            </tr>
        </table>
        </body>
        </html>
        """

    def print_output(self) -> QTextEdit:
        """Generate a HTML report based on the generated output.

        Returns:
            QTextEdit: A QTextEdit widget containing the generated HTML report.
        """

        output = self.output_to_html()

        self.output_window.output_element.clear()
        self.output_window.output_element.setHtml(output)

        return self.output_window.output_element
