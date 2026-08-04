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


def create_new_employee(data):

    is_valid, message = validate_employee(data)

    if not is_valid:
        return {
            "success": False,
            "message": message
        }, 400


    employee = {
        "employeeId": str(uuid.uuid4()),
        "name": data["name"],
        "department": data["department"],
        "email": data["email"],
        "salary": data["salary"]
    }


    create_employee(employee)


    return {
        "success": True,
        "message": "Employee created successfully",
        "data": employee
    }, 201



def list_employees(filters=None):

    filters = filters or {}

    employees = get_all_employees()


    # -------------------------
    # Filtering
    # -------------------------

    department = filters.get("department")
    name = filters.get("name")


    if department:

        employees = [
            emp for emp in employees
            if emp.get("department", "").lower()
            == department.lower()
        ]


    if name:

        employees = [
            emp for emp in employees
            if name.lower()
            in emp.get("name", "").lower()
        ]


    # -------------------------
    # Sorting
    # -------------------------

    sort_by = filters.get("sortBy")
    order = filters.get("order", "asc")


    allowed_sort_fields = [
        "name",
        "department",
        "salary"
    ]


    if sort_by:

        if sort_by not in allowed_sort_fields:

            return {
                "success": False,
                "message":
                f"Invalid sort field. Allowed values: {allowed_sort_fields}"
            }, 400


        reverse_order = (
            order.lower() == "desc"
        )


        employees.sort(
            key=lambda x: x.get(sort_by, ""),
            reverse=reverse_order
        )


    # -------------------------
    # Pagination
    # -------------------------

    try:

        page = int(
            filters.get("page", 1)
        )

        limit = int(
            filters.get("limit", 10)
        )


    except ValueError:

        return {
            "success": False,
            "message":
            "page and limit must be numbers"
        }, 400



    if limit > 50:

        limit = 50


    if page < 1:

        page = 1



    total = len(employees)


    total_pages = (
        math.ceil(total / limit)
        if total > 0
        else 1
    )


    start = (
        page - 1
    ) * limit


    end = start + limit


    employees = employees[start:end]


    return {

        "success": True,

        "page": page,

        "limit": limit,

        "total": total,

        "totalPages": total_pages,

        "data": employees

    }, 200

def find_employee(employee_id):

    employee = get_employee(employee_id)


    if not employee:

        return {
            "success": False,
            "message": "Employee not found"
        }, 404


    return {
        "success": True,
        "data": employee
    }, 200



def modify_employee(employee_id, data):

    is_valid, message = validate_employee(data)


    if not is_valid:

        return {
            "success": False,
            "message": message
        }, 400



    update_employee(
        employee_id,
        data
    )


    return {
        "success": True,
        "message": "Employee updated successfully"
    }, 200



def remove_employee(employee_id):

    delete_employee(employee_id)


    return {
        "success": True,
        "message": "Employee deleted successfully"
    }, 200