import boto3
from botocore.exceptions import ClientError

from config import Config
from logger import (
    log_info,
    log_error
)


dynamodb = boto3.resource(
    "dynamodb",
    region_name=Config.AWS_REGION
)

table = dynamodb.Table(
    Config.EMPLOYEE_TABLE
)


def create_employee(employee):
    """
    Create a new employee in DynamoDB.
    """

    try:
        response = table.put_item(
            Item=employee
        )

        log_info(
            "Employee created in DynamoDB",
            {
                "employeeId": employee["employeeId"]
            }
        )

        return response

    except ClientError as ex:
        log_error(
            "Failed to create employee",
            error=ex,
            data={
                "employeeId": employee.get("employeeId")
            }
        )

        raise


def get_all_employees():
    """
    Retrieve all employees from DynamoDB.
    """

    try:
        response = table.scan()

        items = response.get(
            "Items",
            []
        )

        log_info(
            "Employees retrieved",
            {
                "count": len(items)
            }
        )

        return items

    except ClientError as ex:
        log_error(
            "Failed to retrieve employees",
            error=ex
        )

        raise


def get_employee(employee_id):
    """
    Retrieve a single employee by ID.
    """

    try:
        response = table.get_item(
            Key={
                "employeeId": employee_id
            }
        )

        employee = response.get("Item")

        log_info(
            "Employee retrieved",
            {
                "employeeId": employee_id,
                "found": employee is not None
            }
        )

        return employee

    except ClientError as ex:
        log_error(
            "Failed to retrieve employee",
            error=ex,
            data={
                "employeeId": employee_id
            }
        )

        raise


def update_employee(employee_id, data):
    """
    Update only the fields supplied in the request.
    """

    try:
        update_parts = []
        expression_attribute_names = {}
        expression_attribute_values = {}

        field_mapping = {
            "name": "#name",
            "department": "department",
            "email": "email",
            "salary": "salary"
        }

        for field, value in data.items():
            if field not in field_mapping:
                continue

            attribute_name = field_mapping[field]

            if field == "name":
                expression_attribute_names["#name"] = "name"

            update_parts.append(
                f"{attribute_name} = :{field}"
            )

            expression_attribute_values[
                f":{field}"
            ] = value

        if not update_parts:
            raise ValueError(
                "No fields provided for update"
            )

        update_expression = (
            "SET " + ", ".join(update_parts)
        )

        kwargs = {
            "Key": {
                "employeeId": employee_id
            },
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues":
                expression_attribute_values,
            "ReturnValues": "ALL_NEW"
        }

        # Only send this parameter when it is actually needed.
        if expression_attribute_names:
            kwargs["ExpressionAttributeNames"] = (
                expression_attribute_names
            )

        response = table.update_item(**kwargs)

        log_info(
            "Employee updated in DynamoDB",
            {
                "employeeId": employee_id
            }
        )

        return response.get(
            "Attributes",
            {}
        )

    except ClientError as ex:
        log_error(
            "Failed to update employee",
            error=ex,
            data={
                "employeeId": employee_id
            }
        )
        raise
    
def delete_employee(employee_id):
    """
    Delete an employee from DynamoDB.
    """

    try:
        response = table.delete_item(
            Key={
                "employeeId": employee_id
            },
            ReturnValues="ALL_OLD"
        )

        log_info(
            "Employee deleted from DynamoDB",
            {
                "employeeId": employee_id,
                "deleted": "Attributes" in response
            }
        )

        return response

    except ClientError as ex:
        log_error(
            "Failed to delete employee",
            error=ex,
            data={
                "employeeId": employee_id
            }
        )

        raise