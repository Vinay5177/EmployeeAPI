import json
from logger import log_info, log_error
from employee_service import (
    create_new_employee,
    list_employees,
    find_employee,
    modify_employee,
    remove_employee
)

from utils import response


def lambda_handler(event, context):
    request_id = (
        event
        .get("requestContext", {})
        .get("requestId")
    )

    log_info(
        "Request started",
        {
            "requestId": request_id,
            "event": event
        }
    )


    try:

        # HTTP API Gateway v2 method

        method = (
            event
            .get("requestContext", {})
            .get("http", {})
            .get("method")
        )


        path_parameters = event.get(
            "pathParameters"
        )
        query_params = event.get("queryStringParameters") or {}

        body = {}

        if event.get("body"):

            body = json.loads(
                event["body"]
            )

        log_info(
            "Request details",
            {
                "requestId": request_id,
                "method": method,
                "pathParameters": path_parameters,
                "queryParameters": query_params
            }
        )



        # =========================
        # POST /employees
        # =========================

        if method == "POST":

            result, status = create_new_employee(
                body
            )


        # =========================
        # GET
        # =========================

        elif method == "GET":


            if (
                path_parameters
                and path_parameters.get("employeeId")
            ):

                result, status = find_employee(
                    path_parameters["employeeId"]
                )

            else:

                result, status = list_employees(query_params)



        # =========================
        # PUT
        # =========================

        elif method == "PUT":

            result, status = modify_employee(
                path_parameters["employeeId"],
                body
            )



        # =========================
        # DELETE
        # =========================

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

                "requestId": request_id,

                "statusCode": status

            }

        )

        final_response = response(

            status,

            result

        )

        return final_response



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