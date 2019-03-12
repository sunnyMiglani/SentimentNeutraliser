
# coding: utf-8

# In[1]:


import gensim
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim.downloader as api
import numpy as np
import re
import csv

import pandas as pd
import pprint

import string
import nltk


# In[2]:


pathToDatasets = '../datasets/'
filePath = '../datasets/GoogleNews-vectors-negative300.bin'
word_vectors = api.load("glove-wiki-gigaword-100")
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# In[3]:


from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize



senty = SentimentIntensityAnalyzer()
vocabulary = word_vectors.vocab;


NUMBER_OF_ALTERNATIVES = 5


# ## Utility Code

# In[9]:


def cleanAndTokenizeText(text):
    text = text.lower()
    newString = ""
    for char in text:
        if char not in string.punctuation:
            newString += char
    text = word_tokenize(newString)
    return text;

def listReplacements(word):
    if(word not in vocabulary):
        return []
    possibleReplacements = [word[0] for word in word_vectors.most_similar(word,topn=NUMBER_OF_ALTERNATIVES)]
    return possibleReplacements

def getPOSTags(tweet):
    tags = nltk.pos_tag(tweet)
    return(tags)


# ## NLP Utility Code

# In[27]:


def listReplacements(word):
    if(word not in vocabulary):
        return []
    possibleReplacements = [word[0] for word in word_vectors.most_similar(word,topn=NUMBER_OF_ALTERNATIVES)]
    return possibleReplacements


def posApprovedReplacements(alternativeWords, userTokens, indexOfToken):
    if(alternativeWords == []):
        return []
    tempTokens = userTokens[:]
    truePOSTokens = getPOSTags(tempTokens)
    validWords = []
    
    mainTag = truePOSTokens[indexOfToken][1]
    mainWord = userTokens[indexOfToken]
    
    for ind,word in enumerate(alternativeWords):
        tempTokens[indexOfToken] = word
        posTags = getPOSTags(tempTokens)
        newTag = (posTags[indexOfToken])[1]

        if(str(newTag) == str(mainTag)):
            print("Word {0}[{1}] replaced with {2}[{3}]".format(mainWord, mainTag, word,newTag))
            validWords.append(word)
    return validWords
        


# In[34]:


def getAlternativeSentences(tweet, sentimentOfTweet):
    userInputTokens = cleanAndTokenizeText(tweet)
    print("Alternatives: ")
   
    alternativeStrings = []
    for ind,word in enumerate(userInputTokens):
        
        score = senty.polarity_scores(word)['compound'] # get the aggregated score!
        newUserTokens = userInputTokens[:]
        
        if(score != 0.0):
            replacements = listReplacements(word)       
            replacements = posApprovedReplacements(replacements[:], newUserTokens[:], ind)
            if(replacements == []):
                continue          
            print("Word changed: {0}".format(word));
            for newWord in replacements:
                
                newUserTokens[ind] = newWord;
                newString = ' '.join(newUserTokens)
                sentimentOfNewString = senty.polarity_scores(newString)['compound']
             
            
                if(sentimentOfNewString == 0):
                    continue
                
                alternativeStrings.append(newString)
    return alternativeStrings;


# ## Main Cells

# In[35]:


def runThroughTweets():

    tweets_df = pd.read_csv( pathToDatasets + 'cleanedTweets.csv' , nrows=5, skiprows=72 )

    tweets = tweets_df.values

    for counter,tweet in enumerate(tweets):
        tweet = tweet[0]
        mainSentiment = senty.polarity_scores(tweet)['compound']
        if(mainSentiment == 0):
            continue
        print("\n-NUM({2}) {0}:{1}-\n".format(tweet,mainSentiment, counter))
        newStrings = getAlternativeSentences(tweet, mainSentiment)
        if(newStrings == [] or newStrings == None):
            continue
        for alteredTweet in newStrings:
            sentimentOfNewString = senty.polarity_scores(alteredTweet)['compound']
            if((sentimentOfNewString) >= (mainSentiment)):
                print("{0} : {1} ++POS++".format(alteredTweet,sentimentOfNewString))
#             else:
#                 print("{0} : {1} --NEG--".format(alteredTweet,sentimentOfNewString))
    
    
runThroughTweets()

