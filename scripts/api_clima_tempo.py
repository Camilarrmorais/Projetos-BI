#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from datetime import date, timedelta, datetime, timezone
import json
import pandas as pd
import csv
import os
#import chardet
import spark_configs
import click
from pyspark.sql.functions import  regexp_replace, to_date, to_timestamp, col
import boto3
from pyspark.sql.types import StringType

# Getting data by API
url = f'http://apiadvisor.climatempo.com.br/api/v1/anl/synoptic/locale/BR?token=your-app-token'
print(f'Starting request {url}')
req = requests.get(url)
print(req)