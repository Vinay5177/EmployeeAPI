import boto3


dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("Employees")


def create_employee(employee):
    return table.put_item(
        Item=employee
    )


def get_all_employees():
    response = table.scan()
    return response.get("Items", [])


def get_employee(employee_id):
    response = table.get_item(
        Key={
            "employeeId": employee_id
        }
    )

    return response.get("Item")


def update_employee(employee_id, data):

    return table.update_item(
        Key={
            "employeeId": employee_id
        },
        UpdateExpression="""
        SET #n=:name,
        department=:department,
        email=:email,
        salary=:salary
        """,
        ExpressionAttributeNames={
            "#n": "name"
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