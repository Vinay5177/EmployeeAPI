import json
import logging
import time
from datetime import datetime, timezone

logger = logging.getLogger()

if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

logger.setLevel(logging.INFO)


def _log(level, message, data=None, error=None):
    """
    Writes a structured JSON log entry.
    """

    payload = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "level": level,
        "message": message
    }

    if data is not None:
        payload["data"] = data

    if error is not None:
        payload["error"] = str(error)

    if level == "ERROR":
        logger.error(json.dumps(payload))

    elif level == "WARNING":
        logger.warning(json.dumps(payload))

    else:
        logger.info(json.dumps(payload))


def log_info(message, data=None):
    _log("INFO", message, data=data)


def log_warning(message, data=None):
    _log("WARNING", message, data=data)


def log_error(message, error=None, data=None):
    _log(
        "ERROR",
        message,
        data=data,
        error=error
    )


def start_timer():
    return time.perf_counter()


def elapsed_ms(start_time):
    return round(
        (time.perf_counter() - start_time) * 1000,
        2
    )