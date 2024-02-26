import os
import logging
from datetime import datetime
from enum import Enum


class LogEnvironment(Enum):
    DATABASE = "DATABASE"
    MODELS = "MODELS"
    VIEWS = "VIEWS"
    CONTROLLERS = "CONTROLLERS"
    UTILS = "UTILS"
    TESTS = "TESTS"
    MAIN = "MAIN"
    API = "API"
    TEST = "TEST"


class Logger:
    def __init__(self, isDev: bool):
        """Logger class for logging to a file."""
        self.isdev = isDev
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG if self.isdev else logging.INFO)
        self.env = LogEnvironment

        # Create file handler
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a log file
        self.log_file = os.path.join(
            log_dir, f"{datetime.now().strftime('%Y%m%d')}.log"
        )
        self.file_handler = logging.FileHandler(self.log_file)
        self.file_handler.setLevel(logging.DEBUG)

        # Create a console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG if self.isdev else logging.INFO)

        # Create a formatter and set the formatter for the handlers
        self.formatter = logging.Formatter(
            "%(env)s %(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setFormatter(self.formatter)

        # Add the handlers to the logger
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def log(self, message: str, env: LogEnvironment):
        """Log a message to the log file."""
        self.logger.debug(
            f"{env.value} - {message}",
            exc_info=True,
        )

    def error(self, message: str | Exception, env: LogEnvironment):
        """Log an error to the log file."""
        self.logger.error(
            f"{env.value} - {message}",
            stack_info=True if self.isdev else False,
            exc_info=True,
            stacklevel=2 if self.isdev else 1,
        )

    def warning(self, message: str | Exception, env: LogEnvironment):
        """Log a warning to the log file."""
        self.logger.warning(
            f"{env.value} - {message}",
            stack_info=True if self.isdev else False,
            exc_info=True,
            stacklevel=2 if self.isdev else 1,
        )

    def info(self, message: str, env: LogEnvironment):
        """Log an info message to the log file."""
        self.logger.info(
            f"{env.value} - {message}",
            exc_info=True,
        )

    def critical(self, message: str | Exception, env: LogEnvironment):
        """Log a critical message to the log file."""
        self.logger.critical(
            f"{env.value} - {message}",
            stack_info=True if self.isdev else False,
            exc_info=True,
            stacklevel=2 if self.isdev else 1,
        )

    def exception(self, message: str | Exception, env: LogEnvironment):
        """Log an exception to the log file."""
        self.logger.exception(
            f"{env.value} - {message}",
            stack_info=True if self.isdev else False,
            exc_info=True,
            stacklevel=2 if self.isdev else 1,
        )

    def debug(self, message: str, env: LogEnvironment):
        """Log a debug message to the log file."""
        self.logger.debug(
            f"{env.value} - {message}",
            stack_info=True if self.isdev else False,
            exc_info=True,
            stacklevel=2 if self.isdev else 1,
        )

    def separator(self):
        """Log a separator to the log file."""
        self.logger.debug("--------------------------------------------------")

    def time(self, env: LogEnvironment):
        """Log the current time to the log file."""
        self.logger.debug(f"{env.value} - {datetime.now()}")
