import json

# import requests


def lambda_handler(event, context):
    print(f"Name: {event['name']}")



    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello " + event['name']
            # "location": ip.text.replace("\n", "")
        }),
    }
