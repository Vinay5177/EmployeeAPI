import os


# DynamoDB configuration
TABLE_NAME = os.getenv(
    "TABLE_NAME",
    "Employees"
)


# Environment name
APP_ENV = os.getenv(
    "APP_ENV",
    "local"
)


# AWS Region
AWS_REGION = os.getenv(
    "AWS_REGION",
    "us-east-1"
)