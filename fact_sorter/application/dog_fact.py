"""Handler to handle a dog fact."""

from fact_sorter.application.base.handler import BaseHandler


class DogFactFunction(BaseHandler):
    """Handler to handle a dog fact."""

    def execute(self):
        """Log out dog count and fact."""
        data = self.event["detail"]["fact"]
        count = data.lower().count("dog")
        self.logger.info(
            "The number of times 'dog' occurs in the fact",
            {"dog count": count, "fact": data},
        )


handler = DogFactFunction.handler
