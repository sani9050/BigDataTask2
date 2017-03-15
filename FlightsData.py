
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


# In[10]:

sc


# In[11]:

flightsPath="file:///E:/BIG DATA/FlightsData/flights.csv"


# In[28]:

flights=sc.textFile(flightsPath)


# In[29]:

flights


# In[30]:

flights.count()


# In[15]:

fligths.take(10)


# In[32]:

flightsParsed=fligths.map(lambda x: x.split(','))


# In[33]:

flightsParsed.first()


# In[34]:

from datetime import datetime
from collections import namedtuple

fields = ('date','airline','flightnum','origin','dest','dep','dep_delay','arv','arv_delay','airtime','distance')

Flight = namedtuple('Flight',fields,verbose=True)

DATE_FMT="%Y-%m-%d"

TIME_FMT ="%H%M"

def parse(row):
    row[0] = datetime.strptime(row[0], DATE_FMT).date()
    row[5] = datetime.strptime(row[5], TIME_FMT).time()
    row[6] = float(row[6])
    row[7] = datetime.strptime(row[7], TIME_FMT).time()
    row[8] = float(row[8])
    row[9] = float(row[9])
    row[10]= float(row[10])
    return Flight(*row[:11])


# In[35]:

flightsParsed=flights.map(lambda x: x.split(',')).map(parse)


# In[36]:

flightsParsed.first()


# In[37]:

flightsParsed.map(lambda x:x.distance)


# In[38]:

totalDistance=flightsParsed.map(lambda x:x.distance).reduce(lambda x,y:x+y)


# In[39]:

avgDistance=totalDistance/flightsParsed.count()


# In[40]:

print avgDistance


# In[56]:

fligthsParsed.filter(lambda x:x.dep_delay>0).count()/float(flightsParsed.count())


# In[57]:

flightsParsed.persist()


# In[60]:

sumCount=flightsParsed.map(lambda x:x.dep_delay).aggregate((0,0),
                                                           (lambda some, value: (some[0] + value, some[1]+1)),
                                                           (lambda some1,some2: (some1[0]+some2[0],some1[1]+some2[1])))


# In[61]:

print sumCount


# In[62]:

sumCount[0]/float(sumCount[1])


# In[63]:

flightsParsed.map(lambda x: int(x.dep_delay/60)).countByValue()


# In[ ]:



