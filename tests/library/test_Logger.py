import pytest
from unittest.mock import MagicMock
from library.Logger import Logger, LogEnvironment


@pytest.fixture
def logger():
    return Logger(isDev=True)


def test_log(logger):
    logger.logger.debug = MagicMock()
    message = "This is a log message"
    env = LogEnvironment.MAIN
    logger.log(message, env)
    logger.logger.debug.assert_called_with(
        message,
        extra={"env": env.value},
        exc_info=True,
    )


def test_error(logger):
    logger.logger.error = MagicMock()
    message = "This is an error message"
    env = LogEnvironment.MAIN
    logger.error(message, env)
    logger.logger.error.assert_called_with(
        message,
        extra={"env": env.value},
        stack_info=True,
        exc_info=True,
        stacklevel=2,
    )


def test_warning(logger):
    logger.logger.warning = MagicMock()
    message = "This is a warning message"
    env = LogEnvironment.MAIN
    logger.warning(message, env)
    logger.logger.warning.assert_called_with(
        message,
        extra={"env": env.value},
        stack_info=True,
        exc_info=True,
        stacklevel=2,
    )


def test_info(logger):
    logger.logger.info = MagicMock()
    message = "This is an info message"
    env = LogEnvironment.MAIN
    logger.info(message, env)
    logger.logger.info.assert_called_with(
        message,
        extra={"env": env.value},
        stack_info=False,
        exc_info=True,
        stacklevel=1,
    )


def test_critical(logger):
    logger.logger.critical = MagicMock()
    message = "This is a critical message"
    env = LogEnvironment.MAIN
    logger.critical(message, env)
    logger.logger.critical.assert_called_with(
        message,
        extra={"env": env.value},
        stack_info=True,
        exc_info=True,
        stacklevel=2,
    )


def test_exception(logger):
    logger.logger.exception = MagicMock()
    message = "This is an exception message"
    env = LogEnvironment.MAIN
    logger.exception(message, env)
    logger.logger.exception.assert_called_with(
        message,
        extra={"env": env.value},
        stack_info=True,
        exc_info=True,
        stacklevel=2,
    )


def test_debug(logger):
    logger.logger.debug = MagicMock()
    message = "This is a debug message"
    env = LogEnvironment.MAIN
    logger.debug(message, env)
    logger.logger.debug.assert_called_with(
        message,
        extra={"env": env.value},
        stack_info=True,
        exc_info=True,
        stacklevel=2,
    )
