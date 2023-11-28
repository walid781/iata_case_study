import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
# from delta import DeltaTable

def create_delta_table(database, location_delta, table_name, df, partition=[]):
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .partitionBy(*partition)\
        .save(location_delta)
    spark.sql(f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS `{database}`.`{table_name}`
    USING DELTA LOCATION '{location_delta}'
    TBLPROPERTIES ('table_type' = 'DELTA');
    """)
        
    


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
logger = glueContext.get_logger()
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
df = spark.read.table('test_glue_crawler.csvraw')
df_columns = df.columns
# for col in df_columns:
#     df = df.withColumnRenamed(col, col.replace(' ', '_'))
# spark.sql("CREATE EXTERNAL TABLE IF NOT EXISTS `test_glue_crawler`.`delta_sales_records5` (id int) LOCATION 's3://s3-glue-job-poc/deltaTable/sales_recordsv2/'    TBLPROPERTIES ('classification'='parquet', 'table_type' = 'DELTA');")
# target_table_name = 'delta_sales_recordsv2'
# create_delta_table('test_glue_crawler', 's3://s3-glue-job-poc/deltaTable/sales_recordsv2/', target_table_name, df, partition=['country'])
spark.sql('use test_glue_crawler;')
# create_delta_table(database, location_delta, table_name, df, partition=[]):
df.write \
    .format("parquet") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", "s3://s3-glue-job-poc/deltaTable/sales_recordsv9/")\
    .partitionBy('country')\
    .saveAsTable('sales_recordsv9')
# deltaTableBuilder = (
#             DeltaTable.createIfNotExists(spark) 
#             .tableName('sales_recordsv6')
#             .location('s3://s3-glue-job-poc/deltaTable/sales_recordsv6/')
#             .property(key='delta.enableChangeDataFeed', value='true')
#             .property(key='delta.autoOptimize.autoCompact', value='true')
#             .property(key='delta.autoOptimize.optimizeWrite', value='true')
#             .property(key='delta.columnMapping.mode', value='name')
#             .partitionedBy(['country'])
#         )

# for field in df.schema: 
#     deltaTableBuilder = deltaTableBuilder.addColumn(field.name, field.dataType)
# deltaTableBuilder.execute()



# df.write.partitionBy("country").parquet('s3://s3-glue-job-poc/parquet2/')
job.commit()