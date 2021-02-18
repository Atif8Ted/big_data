import configparser
from pyspark import SparkConf


def get_spark_app_config():
    spark_conf = SparkConf()
    config = configparser.ConfigParser()
    config.read("spark_.conf")
    for (key, val) in config.items("SPARK_CONFIG"):
        spark_conf.set(key, val)
    return spark_conf
