import json

from authorization import is_admin

from employee_service import (
    create_new_employee,
    list_employees,
    find_employee,
    modify_employee,
    remove_employee
)

from exceptions import (
    EmployeeAPIError,
    AuthorizationError,
    ValidationError
)

from utils import build_response

from logger import (
    log_info,
    log_error,
    start_timer,
    elapsed_ms
)

from config import Config


def lambda_handler(event, context):
    timer = start_timer()

    request_context = event.get(
        "requestContext",
        {}
    )

    request_id = request_context.get(
        "requestId",
        "local-test"
    )

    claims = (
        request_context
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )

    user_email = claims.get(
        "email",
        "anonymous"
    )

    role = claims.get(
        "custom:role",
        "unknown"
    )

    method = (
        request_context
        .get("http", {})
        .get("method")
    )

    path = (
        request_context
        .get("http", {})
        .get("path")
    )

    log_info(
        "Request started",
        {
            "environment": Config.ENVIRONMENT,
            "requestId": request_id,
            "user": user_email,
            "role": role,
            "method": method,
            "path": path
        }
    )

    try:
        path_parameters = event.get(
            "pathParameters"
        ) or {}

        query_params = event.get(
            "queryStringParameters"
        ) or {}

        body = {}

        raw_body = event.get("body")

        if raw_body:
            try:
                body = json.loads(
                    raw_body
                )
            except json.JSONDecodeError:
                raise ValidationError(
                    "Request body must contain valid JSON"
                )

            if not isinstance(body, dict):
                raise ValidationError(
                    "Request body must be a JSON object"
                )

        log_info(
            "Request details",
            {
                "requestId": request_id,
                "pathParameters": path_parameters,
                "queryParameters": query_params
            }
        )

        status = 200

        # -------------------------
        # POST
        # -------------------------

        if method == "POST":

            if not is_admin(event):
                raise AuthorizationError(
                    "Admin access required"
                )

            result = create_new_employee(
                body
            )

            status = 201

        # -------------------------
        # GET
        # -------------------------

        elif method == "GET":

            employee_id = path_parameters.get(
                "employeeId"
            )

            if employee_id:
                result = find_employee(
                    employee_id
                )
            else:
                result = list_employees(
                    query_params
                )

        # -------------------------
        # PUT
        # -------------------------

        elif method == "PUT":

            if not is_admin(event):
                raise AuthorizationError(
                    "Admin access required"
                )

            employee_id = path_parameters.get(
                "employeeId"
            )

            if not employee_id:
                raise ValidationError(
                    "employeeId is required"
                )

            result = modify_employee(
                employee_id,
                body
            )

        # -------------------------
        # DELETE
        # -------------------------

        elif method == "DELETE":

            if not is_admin(event):
                raise AuthorizationError(
                    "Admin access required"
                )

            employee_id = path_parameters.get(
                "employeeId"
            )

            if not employee_id:
                raise ValidationError(
                    "employeeId is required"
                )

            result = remove_employee(
                employee_id
            )

        else:
            raise ValidationError(
                "Unsupported method"
            )

        log_info(
            "Request completed",
            {
                "environment": Config.ENVIRONMENT,
                "requestId": request_id,
                "statusCode": status,
                "durationMs": elapsed_ms(timer)
            }
        )

        return build_response(
            status,
            {
                "success": True,
                "data": result,
                "requestId": request_id
            }
        )

    except EmployeeAPIError as ex:

        log_error(
            "API exception",
            error=ex,
            data={
                "requestId": request_id,
                "statusCode": ex.status_code,
                "errorCode": ex.error_code
            }
        )

        return build_response(
            ex.status_code,
            {
                "success": False,
                "errorCode": ex.error_code,
                "message": ex.message,
                "requestId": request_id
            }
        )

    except Exception as ex:

        log_error(
            "Unhandled exception",
            error=ex,
            data={
                "requestId": request_id
            }
        )

        return build_response(
            500,
            {
                "success": False,
                "errorCode": "INTERNAL_ERROR",
                "message": "Internal server error",
                "requestId": request_id
            }
        )