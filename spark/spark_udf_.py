import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, udf
from pyspark.sql.types import StringType

from lib.utils import get_spark_app_config


def parse_gender(gender):
    female_pat = r"^f$|f.m|w.m"
    male_pat = r"^m$|^ma|^m.l"
    if re.search(female_pat, gender.lower()):
        return "Female"
    elif re.search(male_pat, gender.lower()):
        return "Male"
    else:
        return "Unknown"


if __name__ == '__main__':

    try:
        # it is a function which bring all the configuration from a spark_.conf file
        conf = get_spark_app_config()
        spark = SparkSession.builder. \
            config(conf=conf).getOrCreate()
        print("Spark session created")
        parse_gender_udf = udf(parse_gender, StringType())
        df = spark.read.format("csv").option("header", "true").load("data/sample.csv")
        df = df.withColumn("Gender",parse_gender_udf("Gender"))
        print(df.show(truncate=False))
        print(df.printSchema())

    except Exception as e:
        print(e)
