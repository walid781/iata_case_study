import json, os, boto3, pandas as pd
from utils import s3_utils
from io import BytesIO

bucket_name = os.getenv('BUCKET_NAME')


def lambda_handler(event, context):
   
    for record in event['Records']:
        source_bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        s3_object = s3_utils.get_object(bucket_name=source_bucket_name, filename=object_key)
    
        df = pd.read_csv(BytesIO(s3_object))

        temp_dir = '/tmp/' + object_key.replace('.csv', '.parquet')

        df.to_parquet(temp_dir, index=False, compression='gzip', partition_cols=['Country'], engine='pyarrow')
        print(os.listdir(temp_dir))
        s3_utils.uploadDirectory(temp_dir, source_bucket_name, object_key.replace('.csv', '.parquet').replace(os.getenv("RAW_PATH"), os.getenv("PARQUET_PATH")))




    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }

    return response


    