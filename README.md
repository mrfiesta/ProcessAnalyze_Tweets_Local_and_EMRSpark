# Process Analyze Tweets Laptop and with EMR Spark

This repository analize Tweets from two perspectives, with a local machine and a sample dataset, and with AWS EMR Spark with the complete original dataset.

The local machine scenario extract geotagged dataset from a PostgreSQL server and apply a Spatial Query, Remove specific users, Clean symbols, special characters and URL's. Then detect the language of each Tweet, tokenize, remove stop words in dutch and english and steam all the tokens. Finally the script count words, hashtags, bigrams and apply a co-occurrence matrix with selected Terms.

The cloud EMR spark gives the instructions to start a cluster in Amazon CLI with ten m4.4xlarge instances and to run it in cluster mode. Also contain instructuions to configure the Amazon CLI in an Ubuntu OS 18.04. The file Create_EMR_AWScli.sh contains. The instructions to configure CLI and to install a cluster in EMR with Spark, also to sent a python  file contains the variables that have to be adapted to be replicated.

The file TestCloudSparkEMR_firefox_geocode.py




The following are the instructions
