class EmployeeAPIError(Exception):
    """Base exception for the Employee API."""

    status_code = 500
    error_code = "INTERNAL_ERROR"

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(EmployeeAPIError):
    status_code = 400
    error_code = "VALIDATION_ERROR"


class NotFoundError(EmployeeAPIError):
    status_code = 404
    error_code = "NOT_FOUND"


class AuthorizationError(EmployeeAPIError):
    status_code = 403
    error_code = "FORBIDDEN"


class DatabaseError(EmployeeAPIError):
    status_code = 500
    error_code = "DATABASE_ERROR"