import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


        

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'dataBucket'])

sc = SparkContext()
glueContext = GlueContext(sc)
logger = glueContext.get_logger()
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
df = spark.read.table('test_glue_crawler.csvraw')
df_columns = df.columns

spark.sql('use test_glue_crawler;')

df.write \
    .format("parquet") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", f"s3://{args['dataBucket']}/sales_records.parquet/")\
    .partitionBy('country')\
    .saveAsTable('sales_records')




job.commit()