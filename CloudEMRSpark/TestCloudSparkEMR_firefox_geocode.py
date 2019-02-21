# Or the following command
# local findspark.init("opt/spark")
# cloud findspark.init("/usr/local/spark/spark-2.4.0-bin-hadoop2.7")
import os
import re
import json
from operator import add
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.functions import countDistinct, udf
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover
from pyspark.ml import Pipeline
from pyspark.sql.types import *
import pyspark.sql.functions as f
from nltk.stem.porter import *

sc =SparkContext()
sqlContext = SQLContext(sc)

df=sqlContext.read.json('s3://FOLDER_WITH_ALLJSON_FILES/*.json').select('text')
df = df.dropna()
df = df.dropDuplicates()
df = df.withColumn('text',f.regexp_replace('text','[^A-Za-z0-9 @]+', ''))
df = df.withColumn('text',f.regexp_replace('text','http\S+\s*', ''))
df = df.withColumn('text',f.regexp_replace('text','RT|cc', ''))
df = df.withColumn('text',f.regexp_replace('text','@\S+', ''))

geonames = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3://FOLDER_FOR_FILES/NL_geonames_triGram_townprovinces.csv').select(f.lower(f.col('asciiname')),'latitude','longitude')
geonames = geonames.withColumnRenamed("lower(asciiname)", "placename")
geonames = geonames.dropDuplicates(['placename'])

regexTokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W")
# stop words
dutchwords = StopWordsRemover.loadDefaultStopWords('dutch')
englishwords = StopWordsRemover.loadDefaultStopWords('english')
add_stopwords = ["http","https","amp","rt","t","c","the","co","@"]+dutchwords+englishwords
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)
# bag of words count

pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover])
# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(df)
dataset = pipelineFit.transform(df)

########Stemmer definition

dataset1 = dataset.select("filtered")

stemmer = PorterStemmer()

def stem(in_vec):
    out_vec = []
    for t in in_vec:
        t_stem = stemmer.stem(t)
        if len(t_stem) > 2:
            out_vec.append(t_stem)
    return out_vec

# Create user defined function for stemming with return type Array<String>

stemmer_udf = udf(lambda x: stem(x), ArrayType(StringType()))

# Create new df with vectors containing the stemmed tokens
dataset1 = dataset1.withColumn("stemmed", stemmer_udf("filtered"))

#Counting the stemmed words
dataset1.withColumn('wordscounted', f.explode(f.col('stemmed'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(5000).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_wordcount')

#Removing the word Camping and counting
dataset.createOrReplaceTempView("dataset")
dataset2 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text NOT LIKE '%camping%'AND text NOT LIKE '%Camping%'AND text NOT LIKE '%CAMPING%'")
dataset2.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(1000).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_withoutcamping')

#########Co-occurrence matrix files creation
dataset3 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%teken%'OR text LIKE '%Teken%'OR text LIKE '%TEKEN%'")
dataset3.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(1000).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_teken')

dataset4 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%fietsen%'OR text LIKE '%Fietsen%'OR text LIKE '%FIETSEN%'")
dataset4.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_fietsen')

dataset5 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%kamperen%'OR text LIKE '%Kamperen%'OR text LIKE '%KAMPEREN%'")
dataset5.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_kamperen')

dataset6 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%lopen%'OR text LIKE '%Lopen%'OR text LIKE '%LOPEN%'")
dataset6.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_lopen')

dataset7 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%lyme%'OR text LIKE '%Fietsen%'OR text LIKE '%LYME%'")
dataset7.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_lyme')

dataset8 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%spelen%'OR text LIKE '%Spelen%'OR text LIKE '%SPELEN%'")
dataset8.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_spelen')

dataset9 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%teek%'OR text LIKE '%Teek%'OR text LIKE '%TEEK%'")
dataset9.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(1000).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_teek')

dataset10 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%tekenbeet%'OR text LIKE '%Tekenbeet%'OR text LIKE '%TEKENBEET%'")
dataset10.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_tekenbeet')

dataset11 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%tekenbeten%'OR text LIKE '%Tekenbeten%'OR text LIKE '%TEKENBETEN%'")
dataset11.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_tekenbeten')

dataset12 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%wandeling%'OR text LIKE '%Wandeling%'OR text LIKE '%WANDELING%'")
dataset12.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_wandeling')

dataset13 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%wandelen%'OR text LIKE '%Wandelen%'OR text LIKE '%WANDELEN%'")
dataset13.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_wandelen')

dataset14 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%camping%'OR text LIKE '%Camping%'OR text LIKE '%CAMPING%'")
dataset14.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(1000).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_camping')

dataset15 = sqlContext.sql("SELECT filtered, text FROM dataset WHERE text LIKE '%fietstochtn%'OR text LIKE '%Fietstocht%'OR text LIKE '%FIETSTOCHT%'")
dataset15.withColumn('wordscounted', f.explode(f.col('filtered'))).groupBy('wordscounted').count().sort('count', ascending=False).limit(10).coalesce(1).write.format('json').save('s3://FOLDER_FOR_OUTPUT/_fietstocht')

# Unigrams from the complete dataset

unigram = dataset.withColumn('wordscounted', f.explode(f.col('filtered')))
unigram = unigram.select('wordscounted','text')

# Geocode by compare and join Unigrams with Geoplaces

df3 = unigram.join(geonames, [unigram.wordscounted == geonames.placename], how = 'inner' )
df3 = df3.dropDuplicates(['text'])
df3.coalesce(1).write.format('csv').save('s3://FOLDER_FOR_OUTPUT/_geocoded')

sc.stop()
