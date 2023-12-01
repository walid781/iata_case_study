import boto3, json, os
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
    

def upload_fileobj(filename, bucket_name, object_key):
    s3.meta.client.upload_file(filename, bucket_name, object_key)
    

def uploadDirectory(path, bucket_name, s3_folder_path):
        for root,dirs,files in os.walk(path):
            for file in files:
                target_root = root.replace('%20', ' ').replace(path, s3_folder_path)
                upload_fileobj(os.path.join(root,file),bucket_name,f"{target_root}/{file}")