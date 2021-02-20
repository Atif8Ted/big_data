from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

from lib.utils import get_spark_app_config

if __name__ == '__main__':

    try:
        # it is a function which bring all the configuration from a spark_.conf file
        conf = get_spark_app_config()
        spark = SparkSession.builder. \
            config(conf=conf).getOrCreate()
        print("Spark session created")
        df = spark.read.text("data/apache_logs.txt")
        print(df.printSchema())
        log_reg = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\S+) "(\S+)" "([^"]*)'
        logs_df = df.select(regexp_extract('value', log_reg, 1).alias('ip'),
                            regexp_extract('value', log_reg, 4).alias('date'),
                            regexp_extract('value', log_reg, 6).alias('request'),
                            regexp_extract('value', log_reg, 10).alias('referrer'))
        print(df.show(truncate=False))
        print(logs_df.show(truncate=False))
    except Exception as e:
        print(e)
