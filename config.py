import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

"""
This file is used to read the configuration file and store the values in the variables.
--------------------------------------------------------------------------------------

The configuration parameters are stored in a file called config.ini.

The config.ini file contains the following parameters:

[SETUP]

ENV = "Development"

[DATABASE]

FILENAME = "database.db"
DB_TYPE = "SQLite"
DB_NAME = "Sampling Database"


"""

# Read the configuration file

# Setup
ENV = config["SETUP"]["ENV"]

# Database
DB_FILENAME = config["DATABASE"]["FILENAME"]
DB_TYPE = config["DATABASE"]["DB_TYPE"]
DB_NAME = config["DATABASE"]["DB_NAME"]
