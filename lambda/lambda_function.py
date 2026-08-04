import json

from employee_service import (
    create_new_employee,
    list_employees,
    find_employee,
    modify_employee,
    remove_employee
)

from utils import response


def lambda_handler(event, context):

    print("Incoming event:")
    print(json.dumps(event))


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


        body = {}

        if event.get("body"):

            body = json.loads(
                event["body"]
            )


        print("Method:", method)
        print("Path Parameters:", path_parameters)



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

                result, status = list_employees()



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



        return response(
            status,
            result
        )



    except Exception as e:

        print("ERROR:")
        print(str(e))


        return response(
            500,
            {
                "success": False,
                "message": str(e)
            }
        )