"""Handler to handle a dog fact."""

from fact_sorter.application.base.handler import BaseHandler


class DogFactFunction(BaseHandler):
    """Handler to handle a dog fact."""

    def execute(self):
        """Log out the dog fact."""
        data = self.event["detail"]["fact"]
        self.logger.info("Successfully collected dog fact", {"fact": data})


handler = DogFactFunction.handler
