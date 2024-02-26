from datetime import datetime
from unittest.mock import patch
from utils.Logger import Logger, LogEnvironment


def test_logger_info():
    logger = Logger(False)
    message = "This is an info message"

    with patch("logging.Logger.info") as mock_info:
        logger.info(message, LogEnvironment.TEST)
        mock_info.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}", exc_info=True
        )


def test_logger_debug():
    logger = Logger(False)
    message = "This is a debug message"

    with patch("logging.Logger.debug") as mock_debug:
        logger.debug(message, LogEnvironment.TEST)
        mock_debug.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=False,
            exc_info=True,
            stacklevel=1,
        )


def test_logger_debug_dev():
    logger = Logger(True)
    message = "This is a debug message"

    with patch("logging.Logger.debug") as mock_debug:
        logger.debug(message, LogEnvironment.TEST)
        mock_debug.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=True,
            exc_info=True,
            stacklevel=2,
        )


def test_logger_warning():
    logger = Logger(False)
    message = "This is a warning message"

    with patch("logging.Logger.warning") as mock_warning:
        logger.warning(message, LogEnvironment.TEST)
        mock_warning.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=False,
            exc_info=True,
            stacklevel=1,
        )


def test_logger_warning_dev():
    logger = Logger(True)
    message = "This is a warning message"

    with patch("logging.Logger.warning") as mock_warning:
        logger.warning(message, LogEnvironment.TEST)
        mock_warning.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=True,
            exc_info=True,
            stacklevel=2,
        )


def test_logger_error():
    logger = Logger(False)
    message = "This is an error message"

    with patch("logging.Logger.error") as mock_error:
        logger.error(message, LogEnvironment.TEST)
        mock_error.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=False,
            exc_info=True,
            stacklevel=1,
        )


def test_logger_error_dev():
    logger = Logger(True)
    message = "This is an error message"

    with patch("logging.Logger.error") as mock_error:
        logger.error(message, LogEnvironment.TEST)
        mock_error.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=True,
            exc_info=True,
            stacklevel=2,
        )


def test_logger_critical():
    logger = Logger(False)
    message = "This is a critical message"

    with patch("logging.Logger.critical") as mock_critical:
        logger.critical(message, LogEnvironment.TEST)
        mock_critical.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=False,
            exc_info=True,
            stacklevel=1,
        )


def test_logger_critical_dev():
    logger = Logger(True)
    message = "This is a critical message"

    with patch("logging.Logger.critical") as mock_critical:
        logger.critical(message, LogEnvironment.TEST)
        mock_critical.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=True,
            exc_info=True,
            stacklevel=2,
        )


def test_logger_exception():
    logger = Logger(False)
    message = "This is an exception message"

    with patch("logging.Logger.exception") as mock_exception:
        logger.exception(message, LogEnvironment.TEST)
        mock_exception.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=False,
            exc_info=True,
            stacklevel=1,
        )


def test_logger_exception_dev():
    logger = Logger(True)
    message = "This is an exception message"

    with patch("logging.Logger.exception") as mock_exception:
        logger.exception(message, LogEnvironment.TEST)
        mock_exception.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {message}",
            stack_info=True,
            exc_info=True,
            stacklevel=2,
        )


def test_logger_separator():
    logger = Logger(False)

    with patch("logging.Logger.debug") as mock_debug:
        logger.separator()
        mock_debug.assert_called_once_with(
            "--------------------------------------------------"
        )


def test_logger_time():
    logger = Logger(False)

    with patch("logging.Logger.debug") as mock_debug:
        logger.time(LogEnvironment.TEST)
        mock_debug.assert_called_once_with(
            f"{LogEnvironment.TEST.value} - {datetime.now()}"
        )
