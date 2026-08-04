import json
from lambda_function import lambda_handler

event = {
    "requestContext": {
        "http": {
            "method": "DELETE"
        }
    },
    "pathParameters": {
        "employeeId": "ba6d313a-43f6-47c1-8e56-b7bf030e72f8"
    }
}
response = lambda_handler(event, None)

print("Lambda Response:")
print(json.dumps(response, indent=4))