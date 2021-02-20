from pyspark.sql import *
from pyspark.sql.types import StructType, StructField, DateType, StringType, IntegerType

from lib.utils import get_spark_app_config
import logging

if __name__ == '__main__':

    try:
        # it is a function which bring all the configuration from a spark_.conf file
        conf = get_spark_app_config()
        spark = SparkSession.builder. \
            config(conf=conf).getOrCreate()
        print("Spark session created")
        df_csv = spark.read \
            .format("csv") \
            .option("header", "true") \
        .option("inferSchema","true") \
            .load("data/flight*.csv")
        print(df_csv.printSchema())

        # Json

        df_json = spark.read \
            .format("json") \
            .load("data/flight*.json")
        print(df_json.printSchema())

        # PArquet
        df_parquet = spark.read \
            .option("header", "true") \
            .load("data/flight*.parquet")
        print(df_parquet.printSchema())

        # Explicitly setting schema
         # >> two methods to do the same
         #    >> Programatically
         #    >> Using DDL String

        # Programtically setting schema

        flightSchemaStruct = StructType([
            StructField("FL_DATE", DateType()),
            StructField("OP_CARRIER", StringType()),
            StructField("OP_CARRIER_FL_NUM", IntegerType()),
            StructField("ORIGIN", StringType()),
            StructField("ORIGIN_CITY_NAME", StringType()),
            StructField("DEST", StringType()),
            StructField("DEST_CITY_NAME", StringType()),
            StructField("CRS_DEP_TIME", IntegerType()),
            StructField("DEP_TIME", IntegerType()),
            StructField("WHEELS_ON", IntegerType()),
            StructField("TAXI_IN", IntegerType()),
            StructField("CRS_ARR_TIME", IntegerType()),
            StructField("ARR_TIME", IntegerType()),
            StructField("CANCELLED", IntegerType()),
            StructField("DISTANCE", IntegerType())
        ])
        df_csv_schema = spark.read \
            .format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .schema(flightSchemaStruct) \
            .load("data/flight*.csv")

        print(df_csv_schema.printSchema())
        print(df_csv.show(2))

        # Using  DDL Schema
        flightSchemaDDL = """FL_DATE DATE, OP_CARRIER STRING, OP_CARRIER_FL_NUM INT, ORIGIN STRING, 
                  ORIGIN_CITY_NAME STRING, DEST STRING, DEST_CITY_NAME STRING, CRS_DEP_TIME INT, DEP_TIME INT, 
                  WHEELS_ON INT, TAXI_IN INT, CRS_ARR_TIME INT, ARR_TIME INT, CANCELLED INT, DISTANCE INT"""

        df_csv_schema_1 = spark.read \
            .format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
        .option("dateFormat","M/d/y") \
            .schema(flightSchemaDDL) \
            .load("data/flight*.csv")

        print(df_csv_schema_1.printSchema())
        print(df_csv_schema_1.show(2))

    except Exception as e:
        print(e)
