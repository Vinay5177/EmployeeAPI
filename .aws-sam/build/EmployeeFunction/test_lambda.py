import json
import sys
from pathlib import Path

LAMBDA_DIR = Path(__file__).resolve().parent

if str(LAMBDA_DIR) not in sys.path:
    sys.path.insert(0, str(LAMBDA_DIR))

from lambda_function import lambda_handler
import lambda_function


def make_event(method, employee_id=None, role="admin", body=None):
    event = {
        "requestContext": {
            "requestId": "test-request-001",
            "http": {
                "method": method,
                "path": "/employees",
            },
            "authorizer": {
                "jwt": {
                    "claims": {
                        "email": "admin@example.com",
                        "custom:role": role,
                    }
                }
            },
        },
        "pathParameters": {},
        "queryStringParameters": {},
        "body": None,
    }

    if employee_id:
        event["pathParameters"]["employeeId"] = employee_id
        event["requestContext"]["http"]["path"] = (
            f"/employees/{employee_id}"
        )

    if body is not None:
        event["body"] = json.dumps(body)

    return event


def test_get_all_employees(monkeypatch):
    employees = [
        {
            "employeeId": "1",
            "name": "John",
            "department": "IT",
            "email": "john@example.com",
            "salary": 50000,
        }
    ]

    monkeypatch.setattr(
        lambda_function,
        "list_employees",
        lambda filters: {
            "page": 1,
            "limit": 10,
            "total": 1,
            "totalPages": 1,
            "data": employees,
        },
    )

    response = lambda_handler(make_event("GET"), None)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert body["success"] is True
    assert body["data"]["total"] == 1
    assert body["data"]["data"] == employees


def test_get_employee(monkeypatch):
    employee = {
        "employeeId": "6255313d-56df-42c5-bfd4-f6736efc5109",
        "name": "John",
        "department": "IT",
        "email": "john@example.com",
        "salary": 50000,
    }

    monkeypatch.setattr(
        lambda_function,
        "find_employee",
        lambda employee_id: employee,
    )

    event = make_event(
        "GET",
        employee_id=employee["employeeId"],
    )

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert body["success"] is True
    assert body["data"] == employee


def test_create_employee(monkeypatch):
    employee = {
        "employeeId": "new-employee-001",
        "name": "Alice",
        "department": "HR",
        "email": "alice@example.com",
        "salary": 60000,
    }

    monkeypatch.setattr(
        lambda_function,
        "create_new_employee",
        lambda data: employee,
    )

    event = make_event(
        "POST",
        body={
            "name": "Alice",
            "department": "HR",
            "email": "alice@example.com",
            "salary": 60000,
        },
    )

    response = lambda_handler(event, None)

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["success"] is True
    assert body["data"] == employee


def test_non_admin_cannot_delete(monkeypatch):
    delete_called = False

    def fake_delete(employee_id):
        nonlocal delete_called
        delete_called = True

    monkeypatch.setattr(
        lambda_function,
        "remove_employee",
        fake_delete,
    )

    event = make_event(
        "DELETE",
        employee_id="employee-001",
        role="user",
    )

    response = lambda_handler(event, None)

    assert response["statusCode"] == 403

    body = json.loads(response["body"])

    assert body["success"] is False
    assert body["errorCode"] == "FORBIDDEN"
    assert body["message"] == "Admin access required"
    assert delete_called is False


def test_delete_employee(monkeypatch):
    deleted_employee_id = None

    def fake_delete(employee_id):
        nonlocal deleted_employee_id
        deleted_employee_id = employee_id

        return {
            "message": "Employee deleted successfully"
        }

    monkeypatch.setattr(
        lambda_function,
        "remove_employee",
        fake_delete,
    )

    employee_id = "6255313d-56df-42c5-bfd4-f6736efc5109"

    event = make_event(
        "DELETE",
        employee_id=employee_id,
        role="admin",
    )

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert deleted_employee_id == employee_id

    body = json.loads(response["body"])

    assert body["success"] is True
    assert body["data"]["message"] == (
        "Employee deleted successfully"
    )


def test_unsupported_method():
    event = make_event("PATCH")

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["success"] is False
    assert body["errorCode"] == "VALIDATION_ERROR"
    assert body["message"] == "Unsupported method"