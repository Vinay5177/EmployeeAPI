import re


EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"

EMPLOYEE_FIELDS = {
    "name",
    "department",
    "email",
    "salary",
}


def _validate_field(field, value):
    """Validate a single employee field."""

    if field == "name":
        if not isinstance(value, str):
            return False, "Name must be a string"

        if not value.strip():
            return False, "Name cannot be empty"

    elif field == "department":
        if not isinstance(value, str):
            return False, "Department must be a string"

        if not value.strip():
            return False, "Department cannot be empty"

    elif field == "email":
        if not isinstance(value, str):
            return False, "Email must be a string"

        if not re.match(
            EMAIL_PATTERN,
            value.strip()
        ):
            return False, "Invalid email address"

    elif field == "salary":
        try:
            salary = float(value)

            if salary <= 0:
                return False, "Salary must be greater than zero"

        except (TypeError, ValueError):
            return False, "Salary must be a number"

    return True, "Validation successful"


def validate_employee(data):
    """
    Validate a complete employee object.

    Used when creating an employee.
    All employee fields are required.
    """

    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    unknown_fields = set(data.keys()) - EMPLOYEE_FIELDS

    if unknown_fields:
        return False, (
            "Unknown field(s): "
            + ", ".join(sorted(unknown_fields))
        )

    required_fields = [
        "name",
        "department",
        "email",
        "salary",
    ]

    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"

        is_valid, message = _validate_field(
            field,
            data[field]
        )

        if not is_valid:
            return False, message

    return True, "Validation successful"


def validate_employee_update(data):
    """
    Validate a partial employee update.

    At least one valid employee field must be supplied.
    """

    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    if not data:
        return False, "Request body cannot be empty"

    unknown_fields = set(data.keys()) - EMPLOYEE_FIELDS

    if unknown_fields:
        return False, (
            "Unknown field(s): "
            + ", ".join(sorted(unknown_fields))
        )

    for field, value in data.items():
        is_valid, message = _validate_field(
            field,
            value
        )

        if not is_valid:
            return False, message

    return True, "Validation successful"
