import boto3, json
from botocore.exceptions import ClientError
from utils.my_logger import get_logger

logger = get_logger(__file__)

s3 = boto3.resource("s3")

def get_object(bucket_name, filename):
    try:
        obj  = s3.Object(bucket_name=bucket_name, key=filename)
        return obj.get()['Body'].read()
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            logger.error(f'The file {filename} does not exist in the bucket {bucket_name}')
            return None
        else:
            raise ex

def put_object(bucket_name, filename, body = ''):
    obj  = s3.Object(bucket_name=bucket_name, key=filename)
    obj.put(Body=body)


def get_object_as_json(bucket_name, filename):
    content = get_object(bucket_name, filename)
    if content:
        return json.loads(content.decode())
    else:
        return {} 

def set_object_as_json(bucket_name, filename, latest_ingestion):
    put_object(bucket_name, filename, json.dumps(latest_ingestion, indent = 2).encode("ascii"))
    

