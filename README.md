# AVEGA Random 

![GitHub top language](https://img.shields.io/github/languages/top/tlex-web/avega_sampling)
![GitHub](https://img.shields.io/github/license/tlex-web/avega_sampling)
![GitHub last commit](https://img.shields.io/github/last-commit/tlex-web/avega_sampling)
![Lines of code](https://img.shields.io/tokei/lines/github/tlex-web/avega_sampling)


## Description
Random number, random date and monetary unit sampling application

## Development
The application was developed to be used in a Windows environment.

The Frontend was developed using the PySide6 Designer to quickly design the components of the UI. To open the Designer, the following command was used:

```bash
pyqt6-tools designer
``` 

In order to export the UI files of the different components to a Python file, the following command was used:

```bash
pyuic6 %Filename%.ui -o %Filename%.py
```

The Designer allows to create a resource file that can be used to include images in the UI. The resource file can be converted to a Python file using the following command:

```bash
pyside6-rcc -o resources.py view/ui/resources.qrc
```

Note: The resource file needs to be in the same directory as the app.py file in order to import the resources.

## Requirements
1. Python 3.11.8
2. PyQt6 6.2.2
4. requests 2.26.0
5. PyInstaller 4.2

## Tests
The application was tested in a Windows 11 environment using unit tests with *pytest* except for the UI. To run the tests, the following command was used:

```bash
pytest -v -s tests
```

You can also create a coverage report using the following command:

```bash
coverage run -m pytest
```

To see the coverage report, use the following command:

```bash
coverage html
```

The UI was tested manually to ensure that the components were working as expected.

## Installation
1. Create an Executable using *pyinstaller*
2. Copy the Executable to the folder where you want to use it
3. Run the Executable

## Usage
1. Run the Executable
2. Select the type of sampling you want to do
3. Enter the parameters
4. Click on the button to generate the sample
5. The sample will be generated in the same folder as the Executable

## Info 
You can save the parameters and the random seed you used to create samples in a ``config.ini`` file. The application will read the file and use the parameters and seed to generate the sample. The file should be in the same folder as the Executable and should have the following format:

```ini
[ENVIRONMENT]
ENV = "PROD"

[DATABASE]
DB_FILENAME = "database.db"
DB_TYPE = "qsqlite"
DB_NAME = "Sampling Database"

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.