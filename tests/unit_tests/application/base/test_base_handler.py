import pytest
from eventbus_learning.application.base.handler import BaseHandler


class SomeHandler(BaseHandler):
    def execute(self):
        pass


class TestBaseHandler:
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

    def test_execute_is_abstract(self):
        expected_msg = (
            "Can't instantiate abstract class BaseHandler "
            "without an implementation for abstract method 'execute'"
        )

        with pytest.raises(TypeError, match=expected_msg):
            BaseHandler.handler(None, None)
