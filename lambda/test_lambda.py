import json

from lambda_function import lambda_handler


event = {

    "requestContext": {

        "requestId": "local-test-001",

        "http": {
            "method": "DELETE",
            "path": "/employees/{employeeId}"
        },

        "authorizer": {

            "jwt": {

                "claims": {

                    "email": "admin@example.com",
                    "custom:role": "admin"

                }

            }

        }

    },

    "pathParameters": {
        "employeeId": "6255313d-56df-42c5-bfd4-f6736efc5109"
    },

    "body": None

}



response = lambda_handler(
    event,
    None
)



print("\nLambda Response:")

print(
    json.dumps(
        response,
        indent=4
    )
)