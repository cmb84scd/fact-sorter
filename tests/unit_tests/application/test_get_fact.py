import logging
from unittest.mock import MagicMock

import pytest
from eventbus_learning.application.get_fact import GetFactFunction


class TestHandler:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @pytest.fixture
    def handler(self):
        class MockLoggerHandler(GetFactFunction):
            def __init__(self, event, context):
                super().__init__(event, context)

                self.logger = MagicMock(wraps=self.logger)

        yield MockLoggerHandler(None, None)

    def test_returns_an_animal_fact(self, handler, requests_mock):
        url = "http://127.0.0.1:8000/facts"
        response = {"id": 1, "animal": "cat", "fact": "A cat fact."}

        requests_mock.get(url, json=response, status_code=200)

        assert handler.get_fact() == {"animal": "cat", "fact": "A cat fact."}

    def test_logs_out_the_fact(self, handler):
        handler.get_fact = MagicMock(
            return_value={"animal": "cat", "fact": "A cat fact."}
        )

        handler.execute()

        handler.logger.info.assert_called_once_with(
            "The random animal fact is:",
            {"animal": "cat", "fact": "A cat fact."},
        )
