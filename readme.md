# Employee Management System API

A serverless Employee Management REST API built using AWS Lambda, API Gateway, and DynamoDB.

The project demonstrates a production-style serverless architecture with clean separation of responsibilities.

---

## Architecture

```
Client (Postman / Frontend)
          |
          |
          v
Amazon API Gateway
          |
          |
          v
AWS Lambda
          |
          |
          +----------------+
          |                |
          v                v
 Employee Service     Validation
          |
          |
          v
 DynamoDB Helper
          |
          |
          v
 Amazon DynamoDB
```

---

## Technologies Used

- Python 3.14
- AWS Lambda
- Amazon API Gateway (HTTP API)
- Amazon DynamoDB
- Amazon CloudWatch
- Postman
- Git

---

# Project Structure

```
employee-management-system/

├── README.md

└── lambda/

    ├── lambda_function.py
    ├── employee_service.py
    ├── dynamodb_helper.py
    ├── validation.py
    ├── utils.py
    └── test_lambda.py
```

---

# Features

## Employee CRUD Operations

### Create Employee

```
POST /employees
```

Request:

```json
{
    "name": "John Doe",
    "department": "Engineering",
    "email": "john@example.com",
    "salary": 70000
}
```

---

### Get All Employees

```
GET /employees
```

---

### Get Employee By ID

```
GET /employees/{employeeId}
```

---

### Update Employee

```
PUT /employees/{employeeId}
```

Request:

```json
{
    "name": "John Updated",
    "department": "Finance",
    "email": "john.updated@example.com",
    "salary": 80000
}
```

---

### Delete Employee

```
DELETE /employees/{employeeId}
```

---

# Search and Filtering

## Filter by Department

```
GET /employees?department=Engineering
```

---

## Search by Name

```
GET /employees?name=John
```

---

## Combine Filters

```
GET /employees?department=Engineering&name=John
```

---

# Pagination

Employees can be paginated using:

```
GET /employees?page=1&limit=10
```

Example response:

```json
{
    "success": true,
    "page": 1,
    "limit": 10,
    "total": 25,
    "totalPages": 3,
    "data": []
}
```

---

# API Response Format

Successful response:

```json
{
    "success": true,
    "message": "Employee created successfully",
    "data": {}
}
```

Error response:

```json
{
    "success": false,
    "message": "Employee not found"
}
```

---

# Local Testing

Navigate to lambda folder:

```
cd lambda
```

Run:

```
python test_lambda.py
```

---

# AWS Deployment

Deployment steps:

1. Package Lambda files:

```
lambda_function.py
employee_service.py
dynamodb_helper.py
validation.py
utils.py
```

2. Create ZIP package.

3. Upload ZIP to AWS Lambda.

4. Verify handler:

```
lambda_function.lambda_handler
```

5. Test using API Gateway.

---

# AWS Services

## Lambda

Handles API request processing and business logic execution.

## API Gateway

Provides REST endpoints for clients.

## DynamoDB

Stores employee records.

## CloudWatch

Provides logging and monitoring.

---

# Current API Version

Version:

```
v1.0
```

Implemented:

- CRUD operations
- Search
- Filtering
- Pagination
- Serverless deployment

---

# Future Enhancements

Planned features:

- Sorting
- Authentication and authorization
- JWT security
- Unit testing
- AWS SAM deployment
- CI/CD pipeline
- React frontend
- DynamoDB optimization using Query and Indexes

---

# Author

Employee Management System Demo Project