import re


def validate_employee(data):
    """
    Validate employee data.
    """

    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    required_fields = [
        "name",
        "department",
        "email",
        "salary"
    ]

    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"

    # Name validation
    if not isinstance(data["name"], str):
        return False, "Name must be a string"

    if not data["name"].strip():
        return False, "Name cannot be empty"

    # Department validation
    if not isinstance(data["department"], str):
        return False, "Department must be a string"

    if not data["department"].strip():
        return False, "Department cannot be empty"

    # Email validation
    if not isinstance(data["email"], str):
        return False, "Email must be a string"

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(
        email_pattern,
        data["email"].strip()
    ):
        return False, "Invalid email address"

    # Salary validation
    try:
        salary = float(data["salary"])

        if salary <= 0:
            return False, "Salary must be greater than zero"

    except (TypeError, ValueError):
        return False, "Salary must be a number"

    return True, "Validation successful"