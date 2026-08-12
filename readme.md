# Employee Management System API

A serverless Employee Management System REST API built with AWS Lambda, Amazon API Gateway, Amazon Cognito, and Amazon DynamoDB.

## Architecture

```text
Client / Postman
       |
       v
API Gateway HTTP API
       |
       |-- Cognito JWT Authorizer
       |
       v
AWS Lambda
       |
       +---- Authorization / RBAC
       |
       +---- Validation
       |
       +---- Employee Service
       |
       v
Amazon DynamoDB
AWS Services
AWS Lambda
Amazon API Gateway HTTP API
Amazon Cognito User Pool
Amazon DynamoDB
Amazon CloudWatch
AWS SAM
Authentication

The API uses Amazon Cognito JWT authentication.

JWT configuration:

User Pool: EmployeeAPIUserPool
Region: us-east-1
Authorization header:
Authorization: Bearer <ID_TOKEN>

The API validates:

JWT issuer
JWT audience
Token signature
Token expiration
Authorization / RBAC

Two application roles are supported:

User

Users can:

List employees
Retrieve an employee

Users cannot:

Create employees
Update employees
Delete employees
Admin

Admins can:

List employees
Retrieve employees
Create employees
Update employees
Delete employees

The role is read from the Cognito claim:

custom:role
API Endpoints

Base URL:

https://58ghwofkzf.execute-api.us-east-1.amazonaws.com
List employees
GET /employees

Optional query parameters:

?page=1
&limit=10
&department=Engineering
&name=John
&sortBy=salary
&order=desc
Get employee
GET /employees/{employeeId}
Create employee
POST /employees

Example:

{
  "name": "Jane Doe",
  "department": "Engineering",
  "email": "jane@example.com",
  "salary": 80000
}

Admin access required.

Update employee
PUT /employees/{employeeId}

Partial updates are supported.

Example:

{
  "salary": 90000
}

Admin access required.

Delete employee
DELETE /employees/{employeeId}

Admin access required.

Validation

Employee creation requires:

name
department
email
salary

Validation includes:

Required fields
String validation
Empty value checks
Email format validation
Positive salary validation
Unknown field protection
Partial update validation
Pagination

Example:

GET /employees?page=2&limit=5

Response contains:

{
  "page": 2,
  "limit": 5,
  "total": 11,
  "totalPages": 3,
  "data": []
}

Maximum page size is 50.

Filtering

Department:

GET /employees?department=Engineering

Name:

GET /employees?name=John
Sorting

Supported fields:

name
department
salary

Example:

GET /employees?sortBy=salary&order=desc
Error Handling

The API returns structured errors.

Example:

{
  "success": false,
  "errorCode": "FORBIDDEN",
  "message": "Admin access required",
  "requestId": "..."
}

Common error codes:

VALIDATION_ERROR
NOT_FOUND
FORBIDDEN
DATABASE_ERROR
INTERNAL_ERROR

Unauthenticated requests are rejected by API Gateway/Cognito.

Testing

Run the test suite:

python -m pytest .\lambda\test_lambda.py -v

The project includes tests for:

GET employees
GET employee
Create employee
Non-admin DELETE authorization
Admin DELETE
Unsupported HTTP methods
SAM Validation

Validate the SAM template:

sam validate --template-file template.yaml --lint
Build

Build the application:

sam build
Deployment

Deployment configuration is stored in:

samconfig.toml

Deploy:

sam deploy --config-file samconfig.toml --config-env production
CloudWatch Logs

Lambda logs can be viewed with:

aws logs tail /aws/lambda/employee-management-api `
  --region us-east-1 `
  --since 10m
Project Structure
employee-management-system/
│
├── lambda/
│   ├── authorization.py
│   ├── config.py
│   ├── dynamodb_helper.py
│   ├── employee_service.py
│   ├── exceptions.py
│   ├── lambda_function.py
│   ├── logger.py
│   ├── utils.py
│   ├── validation.py
│   └── test_lambda.py
│
├── template.yaml
├── samconfig.toml
└── README.md
Security

The application implements:

JWT authentication
Cognito-based identity
Role-based access control
Admin-only write operations
Request validation
Structured error handling
CloudWatch logging
DynamoDB IAM permissions through SAM
Status

Production deployment verified successfully.

Core CRUD, authentication, authorization, validation, pagination, filtering, sorting, error handling, automated tests, and CloudWatch monitoring have been tested successfully.