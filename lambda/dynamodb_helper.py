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
    Update an existing employee in DynamoDB.
    """

    try:
        response = table.update_item(
            Key={
                "employeeId": employee_id
            },
            UpdateExpression="""
                SET #name = :name,
                    department = :department,
                    email = :email,
                    salary = :salary
            """,
            ExpressionAttributeNames={
                "#name": "name"
            },
            ExpressionAttributeValues={
                ":name": data["name"],
                ":department": data["department"],
                ":email": data["email"],
                ":salary": data["salary"]
            },
            ReturnValues="ALL_NEW"
        )

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