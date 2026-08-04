import json

from employee_service import (
    create_new_employee,
    list_employees,
    find_employee,
    modify_employee,
    remove_employee
)

from utils import response

from logger import (
    log_info,
    log_error
)

from config import APP_ENV


def lambda_handler(event, context):

    request_id = (
        event
        .get("requestContext", {})
        .get("requestId")
    )


    log_info(
        "Request started",
        {
            "environment": APP_ENV,
            "requestId": request_id,
            "event": event
        }
    )


    try:

        method = (
            event
            .get("requestContext", {})
            .get("http", {})
            .get("method")
        )


        path_parameters = event.get(
            "pathParameters"
        )


        query_params = event.get(
            "queryStringParameters"
        ) or {}


        body = {}

        if event.get("body"):

            body = json.loads(
                event["body"]
            )


        log_info(
            "Request details",
            {
                "environment": APP_ENV,
                "requestId": request_id,
                "method": method,
                "pathParameters": path_parameters,
                "queryParameters": query_params
            }
        )


        if method == "POST":

            result, status = create_new_employee(
                body
            )


        elif method == "GET":

            if (
                path_parameters
                and path_parameters.get("employeeId")
            ):

                result, status = find_employee(
                    path_parameters["employeeId"]
                )

            else:

                result, status = list_employees(
                    query_params
                )


        elif method == "PUT":

            result, status = modify_employee(
                path_parameters["employeeId"],
                body
            )


        elif method == "DELETE":

            result, status = remove_employee(
                path_parameters["employeeId"]
            )


        else:

            result = {
                "success": False,
                "message": "Unsupported method"
            }

            status = 400


        log_info(
            "Request completed",
            {
                "environment": APP_ENV,
                "requestId": request_id,
                "statusCode": status
            }
        )


        return response(
            status,
            result
        )


    except Exception as e:

        log_error(
            "Unhandled exception",
            e
        )

        return response(
            500,
            {
                "success": False,
                "message": "Internal server error"
            }
        )