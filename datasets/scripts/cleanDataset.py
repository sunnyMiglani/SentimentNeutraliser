import spacy
import pandas as pd
import csv
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

def removeTwitterData(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'^@\S+','', tweet)
    tweet = re.sub(r'https?\S+','', tweet)
    tweet = tweet.replace("\"", '').replace(',','')

    return tweet

def stemWords(tweet):
    tokenizedTweet = word_tokenize(tweet)
    stemmedWords = list(map(ps.stem, tokenizedTweet))
    tweetAsString = " ".join(str(word) for word in stemmedWords)
    return tweetAsString

def dataClean(tweet):
    tweet = removeTwitterData(tweet)
    tweet = stemWords(tweet)
    
    return tweet


nlp = spacy.load('en')

print("Starting the cleaning!")

with open('twitterDataset.csv', newline='',encoding="ISO-8859-1") as csvfile:
    tweetReader = csv.reader(csvfile)
    listOfTweets = (list(tweetReader))
    print("Size of dataset: {0}".format(len(listOfTweets)))
    listOfTweets = [tweet[5] for tweet in listOfTweets]
    
print(" Going to map the dataCleaning function over the tweets!");
cleanTweets = list(map(dataClean, listOfTweets))
for i in range(0,10):
    print("{0} : {1} \n".format(listOfTweets[i], cleanTweets[i]))

print("--- Done! ---")
df = pd.DataFrame(cleanTweets)

df.to_csv('cleanedTweets.csv')