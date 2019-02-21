from nltk.tokenize import word_tokenize
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


####Define the emoticons and regex

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    # r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
##################Pre-processing
###Stop words compilation
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

###Function to tokenize and stemming

def preprocessEnglish(s, lowercase=False):
    #Remove emoticons, numbers etc. and returns list of cleaned tweets.
    stemmer = PorterStemmer()
    noURL = re.sub("(\w+:\/\/\S+)|^rt|http.+?|^\d+\s|\s\d+\s|\s\d+$|\b\d+\b", '',s)
    tokens = tokenize(noURL)
    lemma = WordNetLemmatizer()
    # print('tokens', tokens)
    lemmtoken = [lemma.lemmatize(i) for i in tokens]
    stemed = [stemmer.stem(i) for i in lemmtoken]
    # print('stemed',stemed)
    if lowercase:
        stemed = [token if emoticon_re.search(token) else token.lower() for token in stemed]
    return stemed

def preprocessDutch(s, lowercase=False):
    #Remove emoticons, numbers etc. and returns list of cleaned tweets.
    stemmer = SnowballStemmer("dutch")
    noURL = re.sub("(\w+:\/\/\S+)|^rt|http.+?|^\d+\s|\s\d+\s|\s\d+$|\b\d+\b", '',s)
    tokens = tokenize(noURL)
    # print(tokens)
    # print('tokens', tokens)
    stemed = [stemmer.stem(i) for i in tokens]
    # print('stemed',stemed)
    if lowercase:
        stemed = [token if emoticon_re.search(token) else token.lower() for token in stemed]
    return stemed
