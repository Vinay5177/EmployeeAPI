import json
from decimal import Decimal


def decimal_converter(obj):

    if isinstance(obj, Decimal):
        return int(obj)

    raise TypeError(
        "Object not JSON serializable"
    )


def response(status_code, body):

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            body,
            default=decimal_converter
        )
    }