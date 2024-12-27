from unittest.mock import patch

import pytest
from fact_sorter.application.base.handler import BaseHandler


class SomeHandler(BaseHandler):
    def execute(self):
        pass


class TestBaseHandler:
    @pytest.fixture
    def mock_logger_class(self):
        logger_path = "fact_sorter.application.base.handler.Logger"

        with patch(logger_path, autospec=True) as mocked_logger:
            yield mocked_logger

    @pytest.fixture
    def mock_logger(self, mock_logger_class):
        yield mock_logger_class()

    @pytest.fixture
    def error_instance(self):
        yield ConnectionError()

    @pytest.fixture
    def ErrorHandler(self, error_instance):
        class Handler(BaseHandler):
            def execute(self):
                raise error_instance

        yield Handler

    def test_init_sets_event_and_context_attrs(self):
        handler = SomeHandler("event", "context")

        assert handler.event == "event"
        assert handler.context == "context"

    def test_handler_sets_event_and_context_attrs_before_execute(self):
        class Handler(BaseHandler):
            def execute(self):
                assert self.event == "event"
                assert self.context == "context"

        Handler.handler("event", "context")

    def test_handler_returns_result_of_execute(self):
        class Handler(BaseHandler):
            def execute(self):
                return "Hello. World!"

        assert Handler.handler(None, None) == "Hello. World!"

    def test_handler_calls_handle_exception_if_execute_throws(self):
        exception = ConnectionError("The connection failed")

        class Handler(BaseHandler):
            def execute(self):
                raise exception

        with patch.object(Handler, "handle_exception") as mock_handle_exc:
            Handler.handler(None, None)
            mock_handle_exc.assert_called_once_with(exception)

    def test_handler_returns_handle_exception_response(self, ErrorHandler):
        with patch.object(ErrorHandler, "handle_exception") as mock_handle_exc:
            mock_handle_exc.return_value = "I can now connect"

            assert ErrorHandler.handler(None, None) == "I can now connect"

    def test_handle_exception_logs_execute_error(
        self, mock_logger, ErrorHandler, error_instance
    ):
        with pytest.raises(Exception):  # noqa: B017 (Using for catching only)
            ErrorHandler.handler(None, None)

        mock_logger.error.assert_called_once_with(
            "Unhandled exception occurred", exception=error_instance
        )

    def test_handle_exception_reraises_error(self, ErrorHandler):
        with pytest.raises(ConnectionError):
            ErrorHandler.handler(None, None)

    def test_execute_is_abstract(self):
        expected_msg = (
            "Can't instantiate abstract class BaseHandler "
            "without an implementation for abstract method 'execute'"
        )

        with pytest.raises(TypeError, match=expected_msg):
            BaseHandler.handler(None, None)
