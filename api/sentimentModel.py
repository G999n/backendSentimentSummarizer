import nltk
nltk.download('twitter_samples')
nltk.download('stopwords')
nltk.download('punkt_tab')

from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import re

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

dict_pos = {}
dict_neg = {}
pos_count = 0
neg_count = 0

for tweet in positive_tweets:
    x = tweet.lower()
    x = re.sub(r'@[\w]+', '', x)
    x = word_tokenize(x)
    x = [token for token in x if token not in string.punctuation]
    x = [word for word in x if word.lower() not in stop_words]
    x = [porter.stem(word) for word in x] 
    for word in x:
        dict_pos[word] = dict_pos.get(word, 1) + 1
        dict_neg[word] = dict_neg.get(word, 1)
        pos_count += 1

for tweet in negative_tweets:
    x = tweet.lower()
    x = re.sub(r'@[\w]+', '', x)
    x = word_tokenize(x)
    x = [token for token in x if token not in string.punctuation]
    x = [word for word in x if word.lower() not in stop_words]
    x = [porter.stem(word) for word in x]
    for word in x:
        dict_neg[word] = dict_neg.get(word, 1) + 1
        dict_pos[word] = dict_pos.get(word, 1)
        neg_count += 1

pos_count += len(dict_pos.keys())
neg_count += len(dict_neg.keys())

def infer_sentiment(text): 
    x = text.lower()
    x = word_tokenize(x)
    x = [token for token in x if token not in string.punctuation]
    x = [word for word in x if word.lower() not in stop_words]
    x = [porter.stem(word) for word in x]

    numerator = 1
    denominator = 1

    for i in x:
        numerator *= dict_pos.get(i, 1) / pos_count
        denominator *= dict_neg.get(i, 1) / neg_count

    val = numerator / denominator
    sentiment = (
        "Positive 😊" if val > 1 else
        "Negative 😠" if val < 1 else
        "Neutral 😐"
    )
    return sentiment, val