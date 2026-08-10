import uuid
import math

from dynamodb_helper import (
    create_employee,
    get_all_employees,
    get_employee,
    update_employee,
    delete_employee
)

from validation import validate_employee

from exceptions import (
    ValidationError,
    NotFoundError,
    DatabaseError
)

from logger import (
    log_info,
    log_error
)


def create_new_employee(data):
    """
    Validate and create a new employee.
    """

    is_valid, message = validate_employee(data)

    if not is_valid:
        log_info(
            "Employee validation failed",
            {
                "reason": message
            }
        )

        raise ValidationError(message)

    employee = {
        "employeeId": str(uuid.uuid4()),
        "name": data["name"].strip(),
        "department": data["department"].strip(),
        "email": data["email"].strip(),
        "salary": data["salary"]
    }

    try:
        create_employee(employee)

        log_info(
            "Employee created",
            {
                "employeeId": employee["employeeId"],
                "department": employee["department"]
            }
        )

        return employee

    except Exception as ex:
        log_error(
            "Failed to create employee",
            error=ex,
            data={
                "employeeId": employee["employeeId"]
            }
        )

        raise DatabaseError(
            "Unable to create employee"
        )


def list_employees(filters=None):
    """
    Retrieve, filter, sort, and paginate employees.
    """

    filters = filters or {}

    try:
        employees = get_all_employees()

        department = filters.get("department")
        name = filters.get("name")

        if department:
            employees = [
                emp
                for emp in employees
                if emp.get("department", "").lower()
                == department.strip().lower()
            ]

        if name:
            employees = [
                emp
                for emp in employees
                if name.strip().lower()
                in emp.get("name", "").lower()
            ]

        sort_by = filters.get("sortBy")
        order = filters.get("order", "asc")

        allowed_sort_fields = [
            "name",
            "department",
            "salary"
        ]

        if sort_by:
            if sort_by not in allowed_sort_fields:
                raise ValidationError(
                    "Invalid sort field. "
                    f"Allowed values: {allowed_sort_fields}"
                )

            reverse_order = (
                str(order).lower() == "desc"
            )

            employees.sort(
                key=lambda employee: employee.get(
                    sort_by,
                    ""
                ),
                reverse=reverse_order
            )

        try:
            page = int(
                filters.get("page", 1)
            )

            limit = int(
                filters.get("limit", 10)
            )

        except (ValueError, TypeError):
            raise ValidationError(
                "page and limit must be numbers"
            )

        if page < 1:
            raise ValidationError(
                "page must be greater than zero"
            )

        if limit < 1:
            raise ValidationError(
                "limit must be greater than zero"
            )

        if limit > 50:
            limit = 50

        total = len(employees)

        total_pages = (
            math.ceil(total / limit)
            if total > 0
            else 1
        )

        start = (page - 1) * limit
        end = start + limit

        employees = employees[start:end]

        log_info(
            "Employees listed",
            {
                "page": page,
                "limit": limit,
                "total": total
            }
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": total_pages,
            "data": employees
        }

    except ValidationError:
        raise

    except Exception as ex:
        log_error(
            "Failed to list employees",
            error=ex
        )

        raise DatabaseError(
            "Unable to retrieve employees"
        )


def find_employee(employee_id):
    """
    Retrieve an employee by ID.
    """

    if not employee_id:
        raise ValidationError(
            "employeeId is required"
        )

    try:
        employee = get_employee(
            employee_id
        )

        if not employee:
            log_info(
                "Employee not found",
                {
                    "employeeId": employee_id
                }
            )

            raise NotFoundError(
                "Employee not found"
            )

        log_info(
            "Employee retrieved",
            {
                "employeeId": employee_id
            }
        )

        return employee

    except NotFoundError:
        raise

    except Exception as ex:
        log_error(
            "Failed to retrieve employee",
            error=ex,
            data={
                "employeeId": employee_id
            }
        )

        raise DatabaseError(
            "Unable to retrieve employee"
        )


def modify_employee(employee_id, data):
    """
    Validate and update an existing employee.
    """

    if not employee_id:
        raise ValidationError(
            "employeeId is required"
        )

    is_valid, message = validate_employee(
        data
    )

    if not is_valid:
        log_info(
            "Employee update validation failed",
            {
                "employeeId": employee_id,
                "reason": message
            }
        )

        raise ValidationError(message)

    try:
        existing_employee = get_employee(
            employee_id
        )

        if not existing_employee:
            log_info(
                "Employee not found for update",
                {
                    "employeeId": employee_id
                }
            )

            raise NotFoundError(
                "Employee not found"
            )

        updated_employee = update_employee(
            employee_id,
            data
        )

        log_info(
            "Employee updated",
            {
                "employeeId": employee_id
            }
        )

        return updated_employee

    except NotFoundError:
        raise

    except Exception as ex:
        log_error(
            "Failed to update employee",
            error=ex,
            data={
                "employeeId": employee_id
            }
        )

        raise DatabaseError(
            "Unable to update employee"
        )


def remove_employee(employee_id):
    """
    Delete an existing employee.
    """

    if not employee_id:
        raise ValidationError(
            "employeeId is required"
        )

    try:
        existing_employee = get_employee(
            employee_id
        )

        if not existing_employee:
            log_info(
                "Employee not found for deletion",
                {
                    "employeeId": employee_id
                }
            )

            raise NotFoundError(
                "Employee not found"
            )

        delete_employee(
            employee_id
        )

        log_info(
            "Employee deleted",
            {
                "employeeId": employee_id
            }
        )

        return {
            "message": "Employee deleted successfully",
            "employeeId": employee_id
        }

    except NotFoundError:
        raise

    except Exception as ex:
        log_error(
            "Failed to delete employee",
            error=ex,
            data={
                "employeeId": employee_id
            }
        )

        raise DatabaseError(
            "Unable to delete employee"
        )