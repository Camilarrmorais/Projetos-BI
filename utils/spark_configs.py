#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Importing libraries
import json
from pyspark.sql import SparkSession
from pyspark import  SparkConf
import boto3


def spark_configs():
    
    #Setting spark configs
    spark_jars = '''
        /root/projetos/utils/jars/mysql-connector-java-5.1.40-bin.jar,
        /root/projetos/utils/jars/redshift-jdbc42-2.1.0.1.jar,
        /root/projetos/utils/jars/postgresql-42.2.5.jre6.jar
    '''

    conf = (
            SparkConf()
            .set('spark.sql.repl.eagerEval.enabled', True)
            .set('spark.sql.execution.arrow.pyspark.enabled', True)
            .set('spark.sql.session.timeZone', 'UTC')
            .set('spark.sql.parquet.int96RebaseModeInRead', 'LEGACY')
            .set('spark.sql.parquet.int96RebaseModeInWrite', 'LEGACY')
            .set('spark.sql.parquet.datetimeRebaseModeInRead', 'LEGACY')
            .set('spark.sql.parquet.datetimeRebaseModeInWrite', 'LEGACY')
            .set('spark.network.timeout', '100000000')
            .set('spark.executor.heartbeatInterval', '100000000')
            .set('spark.executor.memory', '16G') #quanto aloca memória local
            .set('spark.driver.memory', '48G') #quanto de dados pode trafegar
            .set('spark.memory.offHeap.enabled', 'true')
            .set('spark.memory.offHeap.size', '4G' )
            .set('spark.sql.autoBroadcastJoinThreshold', '-1')
            .set('spark.sql.broadcastTimeout', '300000')  
            .set('spark.executor.cores', '8') #quantos cores
            .set('spark.executor.instances', '8')
            .set('spark.default.parallelism', '2') #especifica para rodar 2 fluxos em paralelo
            .set('spark.sql.debug.maxToStringFields', 1000)
            .set('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') #organizar em série
            .set('spark.jars', spark_jars)
            .set('spark.ui.showConsoleProgress', True)
            .set('spark.logConf', True)
            .set('spark.driver.bindAddress', '0.0.0.0')
        )

    spark = (
            SparkSession
            .builder
            .config(conf=conf)
            .master('local[*]')
            .appName('PySpark')
            .getOrCreate()
        )

    return spark
