import json

from lambda_function import lambda_handler



# =====================================
# GET employees test
# Pagination + Sorting
# =====================================


event = {

    "requestContext": {

        "requestId": "local-test-001",

        "http": {

            "method": "GET",

            "path": "/employees"

        }

    },


    "queryStringParameters": {

        "page": "1",

        "limit": "5",

        "sortBy": "salary",

        "order": "desc"

    },


    "pathParameters": None

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