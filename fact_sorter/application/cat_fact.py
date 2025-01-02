"""Handler to handle a cat fact."""

from fact_sorter.application.base.handler import BaseHandler


class CatFactFunction(BaseHandler):
    """Handler to handle a cat fact."""

    def execute(self):
        """Log out the cat fact."""
        data = self.event["detail"]["fact"]
        self.logger.info("Successfully collected cat fact", {"fact": data})


handler = CatFactFunction.handler
