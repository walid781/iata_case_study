import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(sys.argv, ['JOB_NAME', 'dataBucket', 'dataBase', 'csvTable'])

sc = SparkContext()
glueContext = GlueContext(sc)
logger = glueContext.get_logger()
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


spark.sql(f'use {args["dataBase"]};')
df = spark.read.table(args['csvTable'])
df_columns = df.columns

df.write \
    .format("parquet") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", f"s3://{args['dataBucket']}/sales_records.parquet/")\
    .partitionBy('country')\
    .saveAsTable('sales_records')




job.commit()