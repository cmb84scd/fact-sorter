"""Lambda base class."""

import logging
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """Base handler for lambda functions."""

    def __init__(self, event, context):
        """Initialize the handler."""
        self.event = event
        self.context = context
        self.logger = logging.getLogger().setLevel(logging.INFO)

    @abstractmethod
    def execute(self):
        """
        No op.

        Execute the main logic for this lambda. Should be overridden by all
        subclasses.
        """

    @classmethod
    def handler(cls, event, context):
        """
        Lambda handler endpoint.

        This is the entry point for the lambda function. It will create an
        instance of the handler and call the execute method.
        """
        handler = cls(event, context)
        response = handler.execute()
        return response
