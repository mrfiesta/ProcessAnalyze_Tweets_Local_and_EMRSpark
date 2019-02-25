# Process and Analyze Tweets Laptop and with EMR Spark

This repository analize Tweets from two perspectives, with a local machine and a sample dataset, and with AWS EMR Spark with the complete original dataset, based on each user necessities.

Laptop

The local machine scenario extract geotagged dataset from a PostgreSQL server and apply a Spatial Query, Remove specific users, Clean symbols, special characters and URL's. Then detect the language of each Tweet, tokenize, remove stop words in dutch and english and steam all the tokens. Finally the script count words, hashtags, bigrams and apply a co-occurrence matrix with selected Terms.
The file SampleLaptopScenario.py do the following:

1)connect and extract tweets from a PostgreSQL database
2)query the database extracting only the geotagged tweets
3)remove users with more than 3 identical tweets and with more than 3000 tweets
4)remove non alphanumeric characters
5)detect the language between Dutch and English
6)tokenize and remove words from a stop words list
7)apply a stemmer to the tweets
8)group and count all the words in the data set (frequency)
9)count all hashtags in English and Dutch
10)count most frequent bigrams in English and Dutch
11)Deliver a co-occurance matrix within specific element in an array
12)create two charts with most frequent terms in Dutch and the count of elements in dutch and english, also provide a HTML file with an interactive visualization of the geotagged tweets per day.

The instructions to change variables are inside the instructions.txt

EMR

The file Create_EMR_AWScli.sh contains the instructions to configure CLI and to install a cluster in EMR with Spark. Also to sent a pyspark script file that contains a script that process raw Twitter data the variables that have to be adapted to be replicated. The cloud EMR spark gives the instructions to start a cluster in Amazon CLI with ten m4.4xlarge instances (requires to have permission from AMS to request ten instances) and to run it in cluster mode. Also contain instructuions to configure the Amazon CLI in an Ubuntu OS 18.04.

The file TestCloudSparkEMR_firefox_geocode.py do the following:

1)read all the records as JSON objects, 
2)remove special characters (non alphanumeric),
3)remove specific elements of a tweet (URL’s, retweets),
4)remove duplicated Tweets,
5)load a gazetteer with townships and cities of the Netherlands dropping duplicates, 
6)tokenize all the elements, 
7)remove the stop words in Dutch and English, 
8)group and count all the words in the data set (frequency),
9)extract all unigrams and match them with the gazetteer (geocoding), 
10)deliver two files with the most frequent words (JSON) and the geocoded tweets with latitude and longitude coordinates (CSV), and the necessary data to create the co-occurrence matrix (JSON).

The instructions to change variables are inside the instructions.txt
