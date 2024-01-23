import os
import logging
from datetime import datetime


class Logger:
    def __init__(self):
        """Logger class for logging to a file."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # create a file handler
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # create a stream handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create a formatter and add it to the handlers
        formatter = logging.Formatter(
            "%(asctime)s ~ %(levelname)s ~ %(message)s ~ module: %(module)s ~ function: %(module)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str | Exception):
        self.logger.error(message)

    def critical(self, message: str | Exception):
        self.logger.critical(message)
