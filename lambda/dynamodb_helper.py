import boto3

from config import (
    TABLE_NAME,
    AWS_REGION
)


dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)


table = dynamodb.Table(
    TABLE_NAME
)


def create_employee(employee):

    return table.put_item(
        Item=employee
    )


def get_all_employees():

    response = table.scan()

    return response.get(
        "Items",
        []
    )


def get_employee(employee_id):

    response = table.get_item(
        Key={
            "employeeId": employee_id
        }
    )

    return response.get(
        "Item"
    )


def update_employee(employee):

    return table.put_item(
        Item=employee
    )


def delete_employee(employee_id):

    return table.delete_item(
        Key={
            "employeeId": employee_id
        }
    )