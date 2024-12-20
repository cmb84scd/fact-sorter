"""Logger class to ensure consistent logging."""

import json
import logging
import traceback

logging.getLogger().setLevel(logging.INFO)


def default_serializer(value):
    """Serialize provided value to string."""
    try:
        return str(value)
    except Exception:
        return "Unable to serialize to JSON log"


class Logger:
    """Format log records as JSON."""

    def _log(self, level, message, data=None, exception=None):
        """Immediately output the log."""
        method = getattr(logging, level.lower())
        method(self._create_log(level, message, data, exception))

    def info(self, message, data=None, exception=None):
        """Print an INFO log."""
        self._log("INFO", message, data, exception)

    def error(self, message, data=None, exception=None):
        """Print an ERROR log."""
        self._log("ERROR", message, data, exception)

    def _create_log(self, level, message, data=None, exception=None):
        """Format log records as JSON."""
        log = {
            "level": level,
            "message": message,
        }

        if data is not None:
            log["data"] = data

        if exception is not None:
            log["exception"] = self.create_exception_dict(exception)

        return json.dumps(log, default=default_serializer)

    @staticmethod
    def create_exception_dict(exception):
        """Create a standard format dict for logging an error."""
        return {
            "type": type(exception).__name__,
            "traceback": traceback.format_exc(),
        }
