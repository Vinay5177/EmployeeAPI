import logging
import json
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stdout
)


# Reduce AWS SDK noise
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)


def log_info(message, data=None):

    payload = {
        "message": message
    }

    if data:
        payload["data"] = data

    logger.info(
        json.dumps(payload)
    )

    # Force output immediately
    for handler in logger.handlers:
        handler.flush()



def log_error(message, error=None):

    payload = {
        "message": message
    }

    if error:
        payload["error"] = str(error)

    logger.error(
        json.dumps(payload)
    )

    for handler in logger.handlers:
        handler.flush()