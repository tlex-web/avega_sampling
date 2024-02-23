# AVEGA Random 

![GitHub top language](https://img.shields.io/github/languages/top/tlex-web/avega_sampling)
![GitHub](https://img.shields.io/github/license/tlex-web/avega_sampling)
![GitHub last commit](https://img.shields.io/github/last-commit/tlex-web/avega_sampling)
![Lines of code](https://img.shields.io/tokei/lines/github/tlex-web/avega_sampling)


## Description
Random number, random date and monetary unit sampling application

## Installation
1. Create an Executable using pyinstaller
2. Copy the Executable to the folder where you want to use it
3. Run the Executable

## Usage
1. Run the Executable
2. Select the type of sampling you want to do
3. Enter the parameters
4. Click on the button to generate the sample
5. The sample will be generated in the same folder as the Executable

## Info 
You can save the parameters and the random seed you used to create samples in a ``config.json`` file. The application will read the file and use the parameters and seed to generate the sample. The file should be in the same folder as the Executable and should have the following format:

```json
{
    "seed": 123456,
    "parameters": {
        "type": "date",
        "start_date": "2020-01-01",
        "end_date": "2020-12-31",
        "number_of_samples": 10,
        "output_file": "sample.csv"
    }
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.