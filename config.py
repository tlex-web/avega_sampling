import os

"""
This file is used to read the configuration file and store the values in the variables.
--------------------------------------------------------------------------------------

The configuration parameters are stored in a file called config.ini.

"""


# Setup
ENV = "DEV"

# Database
DB_FILENAME = "database.db"
DB_TYPE = "QSQLITE"
DB_NAME = "sampling_db"

# Set configuration parameters

IS_DEV = True if ENV == "DEV" else False

# Set session parameters

SESSION_NAME = os.environ["COMPUTERNAME"]
