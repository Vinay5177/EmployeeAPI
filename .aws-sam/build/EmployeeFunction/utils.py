import json
from decimal import Decimal


def decimal_serializer(obj):
    """
    Convert DynamoDB Decimal values into JSON-compatible numbers.
    """

    if isinstance(obj, Decimal):

        if obj % 1 == 0:
            return int(obj)

        return float(obj)

    raise TypeError(
        f"Object of type {type(obj).__name__} "
        "is not JSON serializable"
    )


def success_response(
    status_code,
    body
):
    """
    Build a successful API Gateway response.
    """

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            body,
            default=decimal_serializer
        )
    }


def error_response(
    status_code,
    message,
    error_code,
    request_id=None
):
    """
    Build an error API Gateway response.
    """

    payload = {
        "success": False,
        "message": message,
        "errorCode": error_code
    }

    if request_id:
        payload["requestId"] = request_id

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            payload,
            default=decimal_serializer
        )
    }


def build_response(
    status_code,
    body
):
    """
    Backward-compatible response builder.
    """

    return success_response(
        status_code,
        body
    )