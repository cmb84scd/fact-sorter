from unittest.mock import ANY, MagicMock

import pytest
import requests
from botocore.stub import Stubber
from eventbus_learning.application.base.logger import Logger
from eventbus_learning.application.get_fact import GetFactFunction

URL = "https://electrical-adelind-catriona-e33e053b.koyeb.app/facts"


class TestHandler:
    @pytest.fixture(autouse=True)
    def logger(self):
        yield MagicMock(wraps=Logger())

    @pytest.fixture
    def handler(self, logger):
        class MockLoggerHandler(GetFactFunction):
            def __init__(self, event, context):
                super().__init__(event, context)

                self.logger = logger

        yield MockLoggerHandler(None, None)

    @pytest.fixture
    def events_stub(self, handler):
        with Stubber(handler.events_client) as stubber:
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

    def test_execute_logs_on_exception_when_get_fact_fails(self, handler):
        exception = Exception("Failed to get fact")
        handler.get_fact = MagicMock(side_effect=exception)
        handler.execute()

        handler.logger.error.assert_called_once_with(
            "Failed to send event to eventbus", exception=exception
        )

    def test_execute_logs_on_exception_when_put_event_fails(
        self, handler, events_stub
    ):
        events_stub.add_client_error(
            "put_events",
            service_error_code="InternalFailure",
            service_message="Failed to put event",
        )

        handler.get_fact = MagicMock(
            return_value={"animal": "cat", "fact": "A cat fact."}
        )
        handler.execute()

        # I'm using ANY as matching the exception object is not easy
        # and I don't feel it's essential to test it in detail.
        handler.logger.error.assert_called_once_with(
            "Failed to send event to eventbus", exception=ANY
        )
