import json, os, boto3, zipfile
from utils import s3_utils
from io import BytesIO

bucket_name = os.getenv('BUCKET_NAME')

glue_client = boto3.client('glue')	
crawler_trigger_name = os.getenv('GLUE_CRAWLER_TRIGGER')

def lambda_handler(event, context):
   
    extracted_file_number = 0
    for record in event['Records']:
        source_bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        s3_object = s3_utils.get_object(bucket_name=source_bucket_name, filename=object_key)
        buffer = BytesIO(s3_object)

        z = zipfile.ZipFile(buffer)
        for filename in z.namelist():
            file_info = z.getinfo(filename)
            s3_utils.put_object(
                bucket_name, 
                f'{os.getenv("RAW_PATH")}{filename}',
                z.open(filename)
            )
            extracted_file_number += 1


    if extracted_file_number:
        glue_client.start_trigger(
            Name=crawler_trigger_name
        )


    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }

    return response


    