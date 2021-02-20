from collections import namedtuple

from pyspark.sql import SparkSession

from big_data_tut.spark.lib.utils import get_spark_app_config

SurveyRecord = namedtuple("SurveyRecord", ['Age', 'Gender', 'Country', 'State'])

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
        # rdds need to sparkcontext
        sc = spark.sparkContext
        lineRDD = sc.textFile('data/sample_no_header.csv')
        # print(lineRDD.collect())
        partitionedRDD = lineRDD.repartition(2)
        colsRDD = partitionedRDD.map(lambda line: line.replace('"', '').split(','))
        selectRDD = colsRDD.map(lambda cols: SurveyRecord(int(cols[1]), cols[1], cols[3], cols[4]))
        filterRDD = selectRDD.filter(lambda r: r.Age < 40)
        kvRDD = filterRDD.map(lambda r: (r.Country, 1))
        countRDD = kvRDD.reduceByKey(lambda v1, v2: v1 + v2)
        colsList = countRDD.collect()
        for i in colsList:
            print(i)
            
    except Exception as e:
        print(e)
