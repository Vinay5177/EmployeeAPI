import re


def validate_employee(data):

    # Required fields
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
    if not data["name"].strip():
        return False, "Name cannot be empty"


    # Department validation
    if not data["department"].strip():
        return False, "Department cannot be empty"


    # Email validation
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, data["email"]):
        return False, "Invalid email address"


    # Salary validation
    try:
        salary = float(data["salary"])

        if salary <= 0:
            return False, "Salary must be greater than zero"

    except:
        return False, "Salary must be a number"


    return True, "Validation successful"