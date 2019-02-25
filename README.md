# Process and Analyze Tweets Laptop and with EMR Spark

This repository analize Tweets from two perspectives, with a local machine and a sample dataset, and with AWS EMR Spark with the complete original dataset, based on each user necessities.

### Laptop

The laptop option, focus on explore a stored dataset with only the geotagged Tweets. By apppliying some regex methods, SQLqueriying, NLP techniques, plotting and mapping. This option is for newbies that want to explore a stored Twitter dataset.

The file SampleLaptopScenario.py do the following:

* Connect and extract tweets from a PostgreSQL database
* Query the database extracting only the geotagged tweets
* Remove users with more than 3 identical tweets and with more than 3000 tweets
* Remove non alphanumeric characters
* Detect the language between Dutch and English
* Tokenize and remove words from a stop words list
* Apply a stemmer to the tweets
* Group and count all the words in the data set (frequency)
* Count all hashtags in English and Dutch
* Count most frequent bigrams in English and Dutch
* Deliver a co-occurance matrix within specific element in an array
* Create two charts with most frequent terms in Dutch and the count of elements in dutch and english, also provide a HTML file with an interactive visualization of the geotagged tweets per day.

The instructions to change variables are inside the instructions.txt

### Amazon EMR

The file Create_EMR_AWScli.sh contains the instructions to configure CLI and to install a cluster in EMR with Spark. Also to sent a pyspark script file that contains a script that process raw Twitter data the variables that have to be adapted to be replicated. The cloud EMR spark gives the instructions to start a cluster in Amazon CLI with ten m4.4xlarge instances (requires to have permission from AMS to request ten instances) and to run it in cluster mode. Also contain instructuions to configure the Amazon CLI in an Ubuntu.

The file TestCloudSparkEMR_firefox_geocode.py do the following:

* Read all the records as JSON objects, 
* Remove special characters (non alphanumeric),
* Remove specific elements of a tweet (URL’s, retweets),
* Remove duplicated Tweets,
* Load a gazetteer with townships and cities of the Netherlands dropping duplicates, 
* Tokenize all the elements, 
* Remove the stop words in Dutch and English, 
* Group and count all the words in the data set (frequency),
* Eextract all unigrams and match them with the gazetteer (geocoding), 
* Deliver two files with the most frequent words (JSON) and the geocoded tweets with latitude and longitude coordinates (CSV), and the necessary data to create the co-occurrence matrix (JSON).

The instructions to change variables are inside the instructions.txt

## Platforms

* **Linux**: Tested on Ubuntu 18.04

## Installation

* **Local**
 * python libraries (pandas, polyglot, nltk, matplotlib, folium)

* **EMR**
  * AWS CLI
  * Have permission to request more than 4 instances on AWS

