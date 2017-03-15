
# coding: utf-8

# In[2]:

import os
import sys


# In[3]:

spark_path = "E:/spark"


# In[4]:

os.environ['SPARK_HOME'] = spark_path


# In[5]:

os.environ['HADOOP_HOME'] = spark_path


# In[6]:

os.environ['PYSPARK_PYTHON'] = sys.executable


# In[7]:

sys.path.append(spark_path + "/bin")
sys.path.append(spark_path + "/python")
sys.path.append(spark_path + "/python/pyspark/")
sys.path.append(spark_path + "/python/lib")
sys.path.append(spark_path + "/python/lib/pyspark.zip")
sys.path.append(spark_path + "/python/lib/py4j-0.10.4-src.zip")


# In[8]:

from pyspark import SparkContext
from pyspark import SparkConf

sc = SparkContext("local", "test")

print sc


# In[9]:

sc


# In[10]:

airlinesPath="file:///E:/BIG DATA/FlightsData/airlines.csv"


# In[11]:

airportsPath="file:///E:/BIG DATA/FlightsData/airports.csv"


# In[12]:

flightsPath="file:///E:/BIG DATA/FlightsData/flights.csv"


# In[14]:

airlines=sc.textFile(airlinesPath)


# In[15]:

print airlines

airline.collect()
# In[17]:

airlines.collect()


# In[18]:

airlines.first()


# In[20]:

airlines.take(10)


# In[21]:

airlines.count()


# In[22]:

airlinesWoHeader = airlines.filter(lambda x:"Description" not in x)


# In[23]:

print airlinesWoHeader


# In[24]:

airlinesWoHeader.take(10)


# In[25]:

airlinesParsed=airlinesWoHeader.map(lambda x:x.split(",")).take(10)


# In[26]:

airlinesParsed


# In[27]:

airlines.map(len).take(10)


# In[28]:

def notHeader(row):
    return "Description" not in row
airlines.filter(notHeader).take(10)


# In[29]:

airlines.filter(notHeader)     .map(lambda x: x.split(','))     .take(10)


# In[30]:

import csv
from StringIO import StringIO

def split(line):
    reader =csv.reader(StringIO(line))
    return reader.next()

airlines.filter(notHeader).map(split).take(10)


# In[31]:

flights=sc.textFile(flightsPath)


# In[32]:

flights.count()


# In[33]:

flights.take(10)


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

totalDistance=flightsParsed.map(lambda x:x.distance).reduce(lambda x,y:x+y)


# In[38]:

avgDistance=totalDistance/flightsParsed.count()


# In[39]:

avgDistance


# In[41]:

flightsParsed.filter(lambda x:x.dep_delay>0).count()/float(flightsParsed.count())


# In[42]:

flightsParsed.persist()


# In[43]:

sumCount=flightsParsed.map(lambda x:x.dep_delay).aggregate((0,0),
                                                           (lambda some, value: (some[0] + value, some[1]+1)),
                                                           (lambda some1,some2: (some1[0]+some2[0],some1[1]+some2[1])))


# In[44]:

print "The average delay is "+str(sumCount[0]/float(sumCount[1]))


# In[45]:

flightsParsed.map(lambda x: int(x.dep_delay/60)).countByValue()


# In[ ]:



