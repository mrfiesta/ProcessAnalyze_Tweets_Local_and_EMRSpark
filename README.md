# ProcessAnalyze_Tweets_Local_and_EMRSpark

These repository analize Tweets from two perspectives, with a local machine and a sample dataset, and with AWS EMR Spark with a original dataset.

The local machine scenario extract geotagged dataset from a PostgreSQL server and apply a Spatial Query, Remove specific users, Clean symbols, special characters and URL's. Then detect the language of each Tweet, tokenize, remove stop words in dutch and english and steam all the tokens. Finally the script count words, hashtags, bigrams and apply a co-occurrence matrix with selected Terms.

The cloud EMR spark gives the instructions to start a cluster in Amazon CLI with 10 m4.4xlarge instances and to run it in cluster mode. The 




The following are the instructions
