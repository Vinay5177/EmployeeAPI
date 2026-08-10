import os


class Config:

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "local"
    )

    AWS_REGION = os.getenv(
        "AWS_REGION",
        "us-east-1"
    )

    EMPLOYEE_TABLE = os.getenv(
        "EMPLOYEE_TABLE",
        "Employees"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )