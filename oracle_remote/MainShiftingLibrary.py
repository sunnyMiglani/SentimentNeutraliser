import SentenceClasses
import ShiftingHelperLibrary

def listReplacements(word):
    if(word not in vocabulary):
        print(" --- {0} not in vocabulary ---".format(word))
        return []
    possibleReplacements = [word[0] for word in word_vectors.most_similar(word,topn=NUMBER_OF_ALTERNATIVES)]
    if(possibleReplacements == []):
        print(" --- No replacements for word {0} ---".format(word))
    antonyms = getAntonymsOfWords(word)
    if(antonyms != []):
        possibleReplacements.extend(antonyms)
        if(VERBOSE_PRINTING): print("Some antonyms for word {0} are {1}".format(word, antonyms[:3]))
        return possibleReplacements
    return possibleReplacements
    
def posApprovedReplacements(alternativeWords, userTokens, indexOfToken):
    if(alternativeWords == []):
        return []
    tempTokens = userTokens[:]
    POSTokens = getPOSTags(tempTokens)
    validWords = []
    
    mainTag = POSTokens[indexOfToken][1]
    mainWord = userTokens[indexOfToken]
    
    for ind,word in enumerate(alternativeWords):
        tempTokens[indexOfToken] = word
        posTags = getPOSTags(tempTokens)
        newTag = (posTags[indexOfToken])[1]
        
        if(str(newTag) == str(mainTag)):
            if(VERBOSE_PRINTING): print("Word {0}[{1}] replaced with {2}[{3}]".format(mainWord, mainTag, word,newTag))
            validWords.append(word)
    if(validWords == [] and VERBOSE_PRINTING):
        print("No POS words found for word {} with tag {}".format(mainWord, mainTag));
    return validWords
        
    
    
def getAlternativeSentences(sentenceObj):
    mainSentence = sentenceObj.ogSentence;
    mainSentiment = sentenceObj.ogSentiment;

    sentenceTokens = cleanAndTokenizeText(mainSentence)

    for ind, word in enumerate(sentenceTokens):
        alternativeSentenceWithHTML = []

        score = senty.polarity_scores(word)['compound']
        copyOfTokens = sentenceTokens[:]
        replacements = []
        if(score != 0.0):
            tempReplacements = listReplacements(word) # get embedding based relations
            if(tempReplacements == []):
                print("No replacements found at all for word {0}".format(word))
                continue
            replacements = posApprovedReplacements(tempReplacements[:], copyOfTokens[:], ind)
            if(replacements == []):
                print(" -- No POS approved words! -- for word {0}\n some non-POS:{1}".format(word, tempReplacements[:4]))
                continue
            sentenceObj.addAlternativesByIndex(ind, replacements)

            ## Generate new sentences by switching that word
            for newWord in replacements:
                htmlFriendlyTokens = copyOfTokens[:]
                copyOfTokens[ind] = newWord
                htmlFriendlyTokens[ind] = cstr("[{0}]".format(newWord), "blue", italics=True);
                newString = ' '.join(copyOfTokens)
                tSentence = SentenceWithHTML(newString, ' '.join(htmlFriendlyTokens))
                alternativeSentenceWithHTML.append(tSentence)
        sentenceObj.addAlternativeStrings(alternativeSentenceWithHTML)
    return sentenceObj

def shiftSentiment(sentenceObj, positive=True):
    
    actualTweet = sentenceObj.ogSentence;
    mainSentiment = sentenceObj.ogSentiment;
    alternateTweets = sentenceObj.alternateSentences;
    
    
    happiestTweet = ""
    saddestTweet = ""
    happiestScore = -sys.maxsize - 1
    saddestScore = sys.maxsize
    correctTweets = []
    
    for tSentence in alternateTweets:
        tweet = tSentence.getSentence();
        newSenty = senty.polarity_scores(tweet)['compound']
        
        if(newSenty < saddestScore):
            saddestTweet = tSentence
            saddestScore = newSenty
        if(newSenty > happiestScore):
            happiestTweet = tSentence
            happiestScore = newSenty
            
        if(newSenty == mainSentiment):
            continue
        if(positive == True):
            if(newSenty > mainSentiment):
                correctTweets.append(tSentence)
                continue
            
            elif(newSenty < mainSentiment):
                continue
                # Grab happiest tweet and if it's not "", then generate more happy tweets from it
        if(positive == False):
            if(newSenty < mainSentiment):
                correctTweets.append(tSentence)
                continue
            
            elif(newSenty > mainSentiment):
                continue
                # grab happiest tweet, and if it's not "", then generate more happy tweets from it
                
    if(correctTweets == []):
        print("\n\nNo tweets found when trying to do Positive={}\n\n".format(positive))
    sentenceObj.resetFinalSentences();
    sentenceObj.addFinalSentences(correctTweets);
    return sentenceObj;


def helper_Combine(mainList, myList):
    newList = []
    for val in myList:
        for mainVal in mainList:
            if(VERBOSE_PRINTING): print("Combining {0} with {1}".format(' '.join(val), ' '.join(mainVal)));
            newList.append(val + mainVal);
    return newList;


def combineSentenceChunks(wholeSentence, dictOfChunks):
    reversedKeys = sorted(dictOfChunks.keys(), reverse=True)
    completeSentences = [];
    mainArr = dictOfChunks[reversedKeys[0]]
    for ind in range(1, len(reversedKeys)):
        key = reversedKeys[ind];
        mainArr = helper_Combine(mainArr, dictOfChunks[key]);
        
    return mainArr;
    
        
def generateSentenceChunks(wholeSentence, keyToChange, nextKey, listOfMyAlternatives):
    newList = list(listOfMyAlternatives)
    newList.append(wholeSentence[keyToChange]);
    generatedSentences = []
#     generatedSentenceObjects = []
    for myAlt in newList:
        newSentence = wholeSentence[:]
        newSentence[keyToChange] = myAlt
#         htmlSentence = newSentence[:]
#         htmlSentence[keyToChange] = cstr("[{0}]".format(newWord), "blue", italics=True);
        if(VERBOSE_PRINTING): print("Generated : {}".format(newSentence[keyToChange:nextKey]))
        generatedSentences.append(newSentence[keyToChange:nextKey]);
#         generatedSentenceObjects.append(SentenceWithHTML(' '.join(htmlSentence),' '.join(newSentence[keyToChange:nextKey])))
        
        
    return generatedSentences
    
    
def getAllPermutations(sentenceObj):
    indexToWordDict = sentenceObj.indexToSetOfWords;
    originalSentence = sentenceObj.ogSentence;
    tokenizedSentence = cleanAndTokenizeText(originalSentence)
    reversedKeys = sorted(indexToWordDict.keys(), reverse=True)
    dictAlternatives  = {}

    keys = sorted(indexToWordDict.keys())
    sentenceChunks = {}
    htmlChunks = {}
    print("Keys : {0}".format(keys))
    
    for ind in range(0,len(keys)):
        key = keys[ind]
        nextKey = keys[ind+1] if ind+1 < len(keys) else len(tokenizedSentence)
        sentenceChunks[key] = generateSentenceChunks(tokenizedSentence, key, nextKey, indexToWordDict[key])
    
    if(keys[0] != 0):
        newList = []
        for thislist in sentenceChunks[keys[0]]:
            newList.append(tokenizedSentence[0:keys[0]] + thislist)
        sentenceChunks[keys[0]] = newList;
        
    print("Sentence Chunks generated!")
        
        
    finalOptions = combineSentenceChunks(tokenizedSentence, sentenceChunks)
    
    
    for val in finalOptions:
        sentence = ' '.join(val)
        score = senty.polarity_scores(sentence)['compound']
        if(score == 0.0):
            continue
        print("{} : {}".format(sentence, score))

if(__name__ == "__main__"):
    print("CAUTION: running the main shifting library! Please refer to git documentation to run this library")
else:
    print("Imported main shifting functions")

'''
 ---------- Example running code 
 ----------  Main imports: 
import gensim.downloader as api
import numpy as np
import re
import csv
import pandas as pd
import pprint
import string
import nltk
import sys
import spacy

from IPython.display import HTML
from nltk.corpus import wordnet 
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

pathToDatasets = '../datasets/'
pathToDataScripts = '../datasets/scripts/'
filePath = '../datasets/GoogleNews-vectors-negative300.bin'

sys.path.insert(0, pathToDataScripts)
from cleanDataset import tokenize_words 

--------- Binaries and models download
print("Should I reload the model?")
tstString = input()
if("no" in tstString.lower()):
    print(" didnt reload model! ")
else:
    print("loading the model!");
    word_vectors = api.load("glove-wiki-gigaword-100")
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

----------- Global Variables

senty = SentimentIntensityAnalyzer()
vocabulary = word_vectors.vocab;

nlp = spacy.load('en')


NUMBER_OF_ALTERNATIVES = 5
TWEET_START = 104
NUM_OF_TWEETS = 5


# VERBOSE_PRINTING = True
VERBOSE_PRINTING = False

USE_SPACY = False
# USE_SPACY = True

COLOR_PRINTING = True
#COLOR_PRINTING = False



punctuation = r"\"#$%&'+-/;<=>?@[\]*.^_`{|}~"

DATE OF VALIDITY: 12th March, 2019.

'''