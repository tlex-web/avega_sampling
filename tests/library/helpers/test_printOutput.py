import pytest
from PyQt6.QtWidgets import QTextEdit
from app import OutputWindow
from library.helpers.printOutput import PrintOutput


@pytest.fixture
def output_window():
    return OutputWindow()


@pytest.fixture
def print_output(output_window):
    company_name = "Sample Company"
    company_year = "2022"
    output = ["Output 1", "Output 2", "Output 3"]
    return PrintOutput(output_window, company_name, company_year, output)


def test_output_to_html(print_output):
    expected_html = """
        <html>
        <head>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }

        h1 {
            text-align: center;
        }
        </style>
        </head>
        <body>
        <h1>Sample Company - 2022</h1>
        <table>
            <tr>
                <th>Output</th>
            </tr>
            <tr>
                <td>['Output 1', 'Output 2', 'Output 3']</td>
            </tr>
        </table>
        </body>
        </html>
        """

    assert print_output.output_to_html() == expected_html


def test_print_output(print_output, output_window):
    expected_output = """
        <html>
        <head>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }

        h1 {
            text-align: center;
        }
        </style>
        </head>
        <body>
        <h1>Sample Company - 2022</h1>
        <table>
            <tr>
                <th>Output</th>
            </tr>
            <tr>
                <td>['Output 1', 'Output 2', 'Output 3']</td>
            </tr>
        </table>
        </body>
        </html>
        """

    output_element = print_output.print_output()

    assert isinstance(output_element, QTextEdit)
    assert output_element.toHtml() == expected_output
    assert output_window.output_element.toHtml() == expected_output
