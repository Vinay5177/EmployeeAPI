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


def update_employee(employee_id, data):
    return table.update_item(

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


def delete_employee(employee_id):

    return table.delete_item(
        Key={
            "employeeId": employee_id
        }
    )