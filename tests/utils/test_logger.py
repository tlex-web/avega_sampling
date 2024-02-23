from unittest.mock import patch
from utils.Logger import Logger


def test_logger_info():
    logger = Logger()
    message = "This is an info message"

    with patch("logging.Logger.info") as mock_info:
        logger.info(message)
        mock_info.assert_called_once_with(message)


def test_logger_debug():
    logger = Logger()
    message = "This is a debug message"

    with patch("logging.Logger.debug") as mock_debug:
        logger.debug(message)
        mock_debug.assert_called_once_with(message)


def test_logger_warning():
    logger = Logger()
    message = "This is a warning message"

    with patch("logging.Logger.warning") as mock_warning:
        logger.warning(message)
        mock_warning.assert_called_once_with(message)


def test_logger_error():
    logger = Logger()
    message = "This is an error message"

    with patch("logging.Logger.error") as mock_error:
        logger.error(message)
        mock_error.assert_called_once_with(message)


def test_logger_critical():
    logger = Logger()
    message = "This is a critical message"

    with patch("logging.Logger.critical") as mock_critical:
        logger.critical(message)
        mock_critical.assert_called_once_with(message)
