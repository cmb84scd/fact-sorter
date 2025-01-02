from unittest.mock import MagicMock

import pytest
from fact_sorter.application.base.logger import Logger
from fact_sorter.application.dog_fact import DogFactFunction


class TestCatFactFunction:
    @pytest.fixture(autouse=True)
    def logger(self):
        yield MagicMock(wraps=Logger())

    @pytest.fixture
    def handler(self, logger):
        class MockLoggerHandler(DogFactFunction):
            def __init__(self, event, context):
                super().__init__(event, context)

                self.logger = logger

        yield MockLoggerHandler(None, None)

    def test_excute_logs_dog_fact(self, handler):
        handler.event = {
            "version": "0",
            "id": "123abc456",
            "detail-type": "fact.retrieved",
            "source": "GetFactFunction",
            "account": "1234567890",
            "time": "2023-01-01T00:00:00Z",
            "region": "an-aws-region",
            "resources": [],
            "detail": {"animal": "dog", "fact": "Dogs bark"},
        }
        expected_data = {"fact": "Dogs bark"}
        handler.execute()

        handler.logger.info.assert_called_once_with(
            "Successfully collected dog fact", expected_data
        )