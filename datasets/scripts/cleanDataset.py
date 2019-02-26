import pandas as pd
import csv
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
punctuation = r"\"#$%&'()+-/:;<=>?[\]^_`{|}~"

def tokenize_words(tweet):
    tweet = removeTwitterData(tweet)
    splitTweet = tweet.split(' ')
    return splitTweet

def removeTwitterData(tweet):
    tweet = tweet.lower()
    newTweet = ""
    for char in tweet:
        if char not in punctuation:
            newTweet+=char
    tweet = newTweet
    tweet = re.sub(r'^@\S+','', tweet) # Remove any twitter mentions from the data
    tweet = re.sub(r'https?\S+','', tweet) # remove any https links
    tweet = re.sub(r'www[\.\w/~]+\S', '', tweet) # remove links that start with www.<name>\~\ .. etc
    tweet = tweet.replace("\"", '').replace(',','') # Replace double quotes, which may mess with text analysis.

    return tweet

def stemWords(tweet):
    # tokenizedTweet = word_tokenize(tweet)
    tokenizedTweet = tokenize_words(tweet)
    print("Tokenized tweet : {}".format(tokenizedTweet))
    stemmedWords = list(map(ps.stem, tokenizedTweet))
    tweetAsString = " ".join(str(word) for word in stemmedWords)
    return tweetAsString

def expandWords(phrase):
    # Taken from https://stackoverflow.com/questions/43018030/replace-apostrophe-short-words-in-python/47091370#47091370
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub(r"i\'ll", "i will", phrase)
    return phrase

def dataClean(tweet):
    decontracted = expandWords(tweet)
    tweet = removeTwitterData(decontracted)
    # tweet = stemWords(tweet)
    
    return tweet

def interaction():
    print("Would you like to enter a string or clean dataset?")
    print("Press 1. for string, 2. for dataset")
    inp = input()
    if("1" in inp):
        tstString = input()
        newString = dataClean(tstString)
        print(newString)
    else:
        print("Starting the cleaning!")
        with open('../twitterDataset.csv', newline='',encoding="ISO-8859-1") as csvfile:
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

        df.to_csv('../cleanedTweets.csv', index = False)

interaction()
