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

    employees = get_all_employees()


    if filters:

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



    # Pagination

    page = int(
        filters.get("page", 1)
        if filters
        else 1
    )


    limit = int(
        filters.get("limit", 10)
        if filters
        else 10
    )


    # Safety limit

    if limit > 50:
        limit = 50


    total = len(employees)


    total_pages = math.ceil(
        total / limit
    ) if total > 0 else 1



    start = (
        page - 1
    ) * limit


    end = start + limit


    paginated_employees = employees[
        start:end
    ]



    return {

        "success": True,

        "page": page,

        "limit": limit,

        "total": total,

        "totalPages": total_pages,

        "data": paginated_employees

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