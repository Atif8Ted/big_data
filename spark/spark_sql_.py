from pyspark.sql import *
from lib.utils import get_spark_app_config
import logging

if __name__ == '__main__':

    try:
        # it is a function which bring all the configuration from a spark_.conf file
        conf = get_spark_app_config()
        spark = SparkSession.builder. \
            config(conf=conf).getOrCreate()
        print("Spark session created")

        # This will print all the configuration that has been defined for the spark
        conf_out = spark.sparkContext.getConf()
        print(conf_out.toDebugString())

        # Finally reading a csv file
        df = spark.read.option("header", "true").csv('data/sample.csv', inferSchema=True)  # Infer schema will try to

        print(df.printSchema())
        # registering it as a tempview

        df.createOrReplaceTempView('survey_tbl')
        groupby_df = spark.sql("select country, count(*) from survey_tbl  group by  country")
        print(groupby_df.show())
    except Exception as e:
        print(e)
