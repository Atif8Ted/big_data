from pyspark.sql import *
from pyspark.sql.functions import spark_partition_id
from pyspark.sql.types import StructType, StructField, DateType, StringType, IntegerType

from lib.utils import get_spark_app_config

# import logging

if __name__ == '__main__':

    try:
        # it is a function which bring all the configuration from a spark_.conf file
        conf = get_spark_app_config()
        spark = SparkSession.builder. \
            config(conf=conf)\
            .enableHiveSupport() \
            .getOrCreate()
        print("Spark session created")

        flightSchemaDDL = """FL_DATE DATE, OP_CARRIER STRING, OP_CARRIER_FL_NUM INT, ORIGIN STRING, 
                          ORIGIN_CITY_NAME STRING, DEST STRING, DEST_CITY_NAME STRING, CRS_DEP_TIME INT, DEP_TIME INT, 
                          WHEELS_ON INT, TAXI_IN INT, CRS_ARR_TIME INT, ARR_TIME INT, CANCELLED INT, DISTANCE INT"""

        df_csv_schema_1 = spark.read \
            .format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("dateFormat", "M/d/y") \
            .schema(flightSchemaDDL) \
            .load("data/flight*.csv")

        print(df_csv_schema_1.printSchema())
        print(df_csv_schema_1.show(2))

        # Now writing to  to the file
        df_csv_schema_1.write \
            .format("parquet") \
            .mode("overwrite") \
            .option("path", "data/csv_to_parquet") \
            .save()
        # avro_format
        df_csv_schema_1.write \
            .format("avro") \
            .mode("overwrite") \
            .option("path", "data/csv_to_avro") \
            .save()
        print(df_csv_schema_1.rdd.getNumPartitions())
        df_csv_schema_1.write \
            .format("json") \
            .mode("overwrite") \
            .option("path", "data/json/") \
            .partitionBy("OP_CARRIER", 'ORIGIN_CITY_NAME') \
            .option("maxRecordsPerFile", 10000) \
            .save()
        # df_csv_schema_1.write.mode("overwrite")\
        #     .bucketBy(5, "OP_CARRIER","ORIGIN") \
        # .sortBy("OP_CARRIER","ORIGIN")\
        # .option("path","spark-warehouse/test_table") \
        #     .saveAsTable("Test_table_")
        df = spark.sql("SELECT * from Test_table_")
        print(df.show(2))
        # print(df.printSchema())
    except Exception as e:
        print(e)
