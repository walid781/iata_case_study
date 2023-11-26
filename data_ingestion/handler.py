import json, os, requests, boto3
from utils import s3_utils

url = 'https://eforexcel.com/wp/wp-content/uploads/2020/09/2m-Sales-Records.zip'
bucket_name = os.getenv('BUCKET_NAME')

def lambda_handler(event, context):
   

    res = requests.get(url)

    if res.status_code == 200:
        s3_utils.put_object(bucket_name, 'RAW/file.zip', body=res.content)



    response = {
        "statusCode": 200,
        "body": json.dumps('body')
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