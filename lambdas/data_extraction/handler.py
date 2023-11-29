import json, os, boto3, zipfile
from utils import s3_utils
from io import BytesIO

url = 'https://eforexcel.com/wp/wp-content/uploads/2020/09/2m-Sales-Records.zip'
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


#This will give you list of files in the folder you mentioned as prefix
# s3_resource = boto3.resource('s3')
# #Now create zip object one by one, this below is for 1st file in file_list
# zip_obj = s3_resource.Object(bucket_name=bucket, key=file_list[0])
# print (zip_obj)
# buffer = BytesIO(zip_obj.get()["Body"].read())

# z = zipfile.ZipFile(buffer)
# for filename in z.namelist():
#     file_info = z.getinfo(filename)
#     s3_resource.meta.client.upload_fileobj(
#         z.open(filename),
#         Bucket=bucket,
        # Key='result_files/' + f'{filename}')
    