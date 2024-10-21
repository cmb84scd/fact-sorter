import logging
from unittest.mock import MagicMock

import pytest
import requests
from botocore.stub import Stubber
from eventbus_learning.application.get_fact import GetFactFunction

URL = "http://127.0.0.1:8000/facts"


class TestHandler:
    @pytest.fixture(autouse=True)
    def logger(self):
        logger = logging.getLogger().setLevel(logging.INFO)
        yield MagicMock(wraps=logger)

    @pytest.fixture
    def handler(self, logger):
        class MockLoggerHandler(GetFactFunction):
            def __init__(self, event, context):
                super().__init__(event, context)

                self.logger = logger

        yield MockLoggerHandler(None, None)

    @pytest.fixture
    def events_stub(self, handler):
        with Stubber(handler.event_bus_client) as stubber:
            yield stubber

        # Confirm tests made all expected requests
        stubber.assert_no_pending_responses()

    def test_returns_an_animal_fact(self, handler, requests_mock):
        response = {"id": 1, "animal": "cat", "fact": "A cat fact."}

        requests_mock.get(URL, json=response, status_code=200)

        assert handler.get_fact() == {"animal": "cat", "fact": "A cat fact."}

    def test_get_fact_raises_on_connection_error(self, handler, requests_mock):
        requests_mock.get(URL, exc=requests.exceptions.ConnectionError)

        with pytest.raises(requests.exceptions.ConnectionError) as e:
            handler.get_fact()

        handler.logger.error.assert_called_once_with(
            "Failed to connect to API", exception=e.value
        )

    def test_get_fact_raises_on_timeout_error(self, handler, requests_mock):
        requests_mock.get(URL, exc=requests.exceptions.Timeout)

        with pytest.raises(requests.exceptions.RequestException) as e:
            handler.get_fact()

        handler.logger.error.assert_called_once_with(
            "Failed to get fact", exception=e.value
        )

    def test_get_fact_raises_on_no_data_returned(self, handler, requests_mock):
        requests_mock.get(URL, status_code=404)

        with pytest.raises(requests.exceptions.HTTPError) as e:
            handler.get_fact()

        handler.logger.error.assert_called_once_with(
            "No data returned", {"Status Code": 404}, exception=e.value
        )

    def test_puts_the_fact_on_the_event_bus(self, handler, events_stub):
        response = {"Entries": [{"EventId": "1"}], "FailedEntryCount": 0}
        event = {
            "Detail": "{'animal': 'cat', 'fact': 'A cat fact.'}",
            "DetailType": "fact.retrieved",
            "EventBusName": handler.EVENT_BUS_ARN,
            "Source": "GetFactFunction",
        }
        expected_params = {"Entries": [event]}

        events_stub.add_response("put_events", response, expected_params)

        expected_info_log = ["Sending fact to eventbus", event]

        handler.get_fact = MagicMock(
            return_value={"animal": "cat", "fact": "A cat fact."}
        )
        handler.execute()

        handler.logger.info.assert_called_once_with(*expected_info_log)
