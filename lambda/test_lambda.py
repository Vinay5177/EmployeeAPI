import json
from lambda_function import lambda_handler

event = {
    "requestContext": {
        "http": {
            "method": "GET"
        }
    },
    "queryStringParameters": {
    "department": "Engineering",
    "name": "John"
}
}

response = lambda_handler(event, None)

print(json.dumps(response, indent=4))
print("\nParsed Body:")
print(json.dumps(json.loads(response["body"]), indent=4))