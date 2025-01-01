"""Handler to handle a cat fact."""

from fact_sorter.application.base.handler import BaseHandler


class CatFactHandler(BaseHandler):
    """Handler to handle a cat fact."""

    def execute(self):
        """Log out the cat fact."""
        self.logger.info("Cat fact retrieved", self.event)


handler = CatFactHandler.handler
