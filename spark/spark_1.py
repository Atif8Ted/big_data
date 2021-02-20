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
        # read small part of file and infer data types

        # print(df.show(truncate=False))
        print(df.printSchema())
        filter_df = df.where("Age<40").select("Age", "Gender", 'Country', 'state')
        logging.info(filter_df.show())
        groupby_df = filter_df.groupBy("Country").count()
        logging.info(groupby_df.show())
        print(groupby_df.collect())
        # repartitonng our dataframe
        partitioned_df = filter_df.repartition(2)
        group_by_df = partitioned_df.groupBy('Country').count()
        print(group_by_df.show())
        input("")

        spark.stop()
    except Exception as e:
        print(e)
