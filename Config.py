
# coding: utf-8

# In[1]:

import os
import sys


# In[2]:

spark_path = "E:/spark"


# In[3]:

os.environ['SPARK_HOME'] = spark_path


# In[4]:

os.environ['HADOOP_HOME'] = spark_path


# In[5]:

os.environ['PYSPARK_PYTHON'] = sys.executable


# In[6]:

sys.path.append(spark_path + "/bin")
sys.path.append(spark_path + "/python")
sys.path.append(spark_path + "/python/pyspark/")
sys.path.append(spark_path + "/python/lib")
sys.path.append(spark_path + "/python/lib/pyspark.zip")
sys.path.append(spark_path + "/python/lib/py4j-0.10.4-src.zip")


# In[7]:

from pyspark import SparkContext
from pyspark import SparkConf


# In[8]:

conf = SparkConf()
conf.set("spark.executor.memory", "2g")
conf.set("spark.cores.max", "4")

sc = SparkContext("local", conf=conf)


# In[9]:

print sc


# In[ ]:



