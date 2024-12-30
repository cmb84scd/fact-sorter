import os
from datetime import datetime
from unittest.mock import ANY, patch

import pytest
from fact_sorter.application.base import logger as lambda_logger

logging_path = "fact_sorter.application.base.logger.logging"


class NotStringable:
    def __str__(self):
        pass


class TestLogger:
    @pytest.fixture
    def mock_logging(self):
        with patch(logging_path, autospec=True) as mocked_logging:
            yield mocked_logging

    @pytest.fixture
    def logger(self):
        yield lambda_logger.Logger()

    @pytest.fixture
    def logger_with_mock_create_exception_dict(self, logger):
        def create_exception_dict(exception):
            return {
                "type": type(exception).__name__,
                "traceback": "Test error traceback",
            }

        logger.create_exception_dict = create_exception_dict
        yield logger

    def test_info_logs_expected_output(
        self, logger_with_mock_create_exception_dict, mock_logging
    ):
        exception = ConnectionError("The connection failed")
        logger_with_mock_create_exception_dict.info(
            "This is a test", {"test": 1}, exception=exception
        )

        expected_log = (
            "{"
            '"level": "INFO", '
            '"message": "This is a test", '
            '"data": {"test": 1}, '
            '"exception": {'
            '"type": "ConnectionError", '
            '"traceback": "Test error traceback"'
            "}"
            "}"
        )

        mock_logging.info.assert_called_once_with(expected_log)

    def test_error_logs_expected_output(
        self, logger_with_mock_create_exception_dict, mock_logging
    ):
        exception = ConnectionError("The connection failed")
        logger_with_mock_create_exception_dict.error(
            "This is a test error", {"error": 1}, exception=exception
        )

        expected_log = (
            "{"
            '"level": "ERROR", '
            '"message": "This is a test error", '
            '"data": {"error": 1}, '
            '"exception": {'
            '"type": "ConnectionError", '
            '"traceback": "Test error traceback"'
            "}"
            "}"
        )

        mock_logging.error.assert_called_once_with(expected_log)

    def test_create_log_returns_expected_json(self, logger, mock_logging):
        returned_log = logger._create_log(
            "INFO",
            "Test message",
            {"bool": True, "num": 5, "arr": [5, 6, 7], "null": None},
        )

        expected_log = (
            "{"
            '"level": "INFO", '
            '"message": "Test message", '
            '"data": {'
            '"bool": true, '
            '"num": 5, '
            '"arr": [5, 6, 7], '
            '"null": null'
            "}"
            "}"
        )

        assert returned_log == expected_log

    def test_create_log_handles_non_json(self, logger, mock_logging):
        template = '{{"level": "ERROR", "message": "Test", "data": {}}}'

        expected_log1 = template.format('"{5, 6, 7}"')
        expected_log2 = template.format('"Unable to serialize to JSON log"')
        expected_log3 = template.format('{"datetime": "2024-12-05 17:00:00"}')
        expected_log4 = template.format(
            '{"whoops": "Unable to serialize to JSON log"}'
        )

        returned_log1 = logger._create_log("ERROR", "Test", set([5, 6, 7]))
        returned_log2 = logger._create_log("ERROR", "Test", NotStringable())
        returned_log3 = logger._create_log(
            "ERROR", "Test", {"datetime": datetime(2024, 12, 5, 17)}
        )
        returned_log4 = logger._create_log(
            "ERROR", "Test", {"whoops": NotStringable()}
        )

        assert returned_log1 == expected_log1
        assert returned_log2 == expected_log2
        assert returned_log3 == expected_log3
        assert returned_log4 == expected_log4

    def test_create_exception_dict(self):
        logger = lambda_logger.Logger()
        expected_dict = {
            "type": "ConnectionError",
            "traceback": ANY,
        }
        file_path = os.path.abspath(__file__)

        try:
            raise ConnectionError("The connection failed")
        except Exception as e:
            exception_dict = logger.create_exception_dict(e)

        traceback = exception_dict["traceback"]

        assert exception_dict == expected_dict
        assert traceback.startswith("Traceback (most recent call last):")
        assert file_path in traceback
