import json, os, requests, boto3
from utils import s3_utils

url = 'https://eforexcel.com/wp/wp-content/uploads/2020/09/2m-Sales-Records.zip'
bucket_name = os.getenv('BUCKET_NAME')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def lambda_handler(event, context):
   

    print(event)

    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """