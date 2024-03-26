import logging
import os
import sys
from datetime import datetime
from utils.Logger import Logger, LogEnvironment


def test_logger_init():
    logger = Logger(isDev=True)
    assert logger.isdev == True
    assert logger.logger.level == logging.DEBUG
    assert logger.logger.propagate == False


def test_logger_handle_exception():
    logger = Logger(isDev=True)

    class CustomException(Exception):
        pass

    try:
        raise CustomException("Custom exception message")
    except CustomException as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.handle_exception(exc_type, exc_value, exc_traceback)

    log_file = os.path.join(
        os.getcwd(), "logs", f"{datetime.now().strftime('%Y%m%d')}.log"
    )
    with open(log_file, "r") as file:
        log_content = file.read()

    assert "CustomException: Custom exception message" in log_content


def test_logger_log():
    logger = Logger(isDev=True)
    logger.log("Log message", LogEnvironment.MAIN)


def test_logger_error():
    logger = Logger(isDev=True)
    logger.error("Error message", LogEnvironment.MAIN)


def test_logger_warning():
    logger = Logger(isDev=True)
    logger.warning("Warning message", LogEnvironment.MAIN)


def test_logger_info():
    logger = Logger(isDev=True)
    logger.info("Info message", LogEnvironment.MAIN)


def test_logger_critical():
    logger = Logger(isDev=True)
    logger.critical("Critical message", LogEnvironment.MAIN)


def test_logger_exception():
    logger = Logger(isDev=True)
    logger.exception("Exception message", LogEnvironment.MAIN)


def test_logger_debug():
    logger = Logger(isDev=True)
    logger.debug("Debug message", LogEnvironment.MAIN)


def test_logger_separator():
    logger = Logger(isDev=True)
    logger.separator()


def test_logger_time():
    logger = Logger(isDev=True)
    logger.time(LogEnvironment.MAIN)
