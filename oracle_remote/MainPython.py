#!/usr/bin/env python
# coding: utf-8

# ## Import Statements

# In[16]:


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
import pickle
import os

from flask import Flask, render_template
from flask_cors import CORS
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
app = Flask(__name__, template_folder="website_resources/")
CORS(app)

from cleanDataset import tokenize_words, dataClean


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:70% !important; }</style>"))


# ## Downloading binaries and models
# 

# In[17]:
RUN_AS_MAIN = False

if(__name__ == "__main__"):
    RETURN_HTML_REPLACEMENT = []
    RUN_AS_MAIN = True


print("Should I reload the model?")
tstString = "";
if(RUN_AS_MAIN):
    print("Loading the model as the name is main!")
    tstString = "yes"
else:
    tstString = input()
if("no" in tstString.lower() or "n" in tstString.lower()):
    print(" didnt reload model! ")
else:
    print("loading the model!");

    print("Loading gigaword-300")
    if(os.path.exists("../datasets/word_vectors-300.pickle")):
        print("loading via pickle!")
        pickle_in = open("../datasets/word_vectors-300.pickle", "rb")
        word_vectors = pickle.load(pickle_in);
    else:
        print("loaded without pickle")
        print("-- LOADING GIGAWORD-100 TO SAVE TIME --")
        word_vectors = api.load("glove-wiki-gigaword-100")
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    print("Model Loaded!")


# ## Global Variables and Global Objects

# In[18]:


senty = SentimentIntensityAnalyzer()
vocabulary = word_vectors.vocab;

nlp = spacy.load('en')


NUMBER_OF_ALTERNATIVES = 5
TWEET_START = 1
NUM_OF_TWEETS = 30


# VERBOSE_PRINTING = True
VERBOSE_PRINTING = False

# USE_SPACY = False
USE_SPACY = True

COLOR_PRINTING = True
#COLOR_PRINTING = False

# PRINT_NEUTRAL = True
PRINT_NEUTRAL = False

PRINT_ALL_STRINGS = True
# PRINT_ALL_STRINGS = False

SHOW_ALTS = 30

punctuation = r"\"#$%&'+-/;<=>?@[\]*^_`{|}~"



# ## Class for Sentences
# 

# In[19]:


from SentenceClass import *


# ## Utility Code

# In[20]:



def printStrings(sentenceObj):
    
    numberOfPrints = 0
    newStrings = generateHTMLObjectsFromSentence(sentenceObj)
    mainSentiment = sentenceObj.ogSentiment;
    listOfSentencesWithSentiments = []
    bestSentiment = -sys.maxsize - 1
    worstSentiment = sys.maxsize
    
    bestSentimentString = "";
    worstSentimentString = "";
    
    
    for ind, tSentence in enumerate(newStrings):
            alteredTweet = tSentence.getSentence()
            htmlText = tSentence.getHTML()
            sentimentOfNewString = senty.polarity_scores(alteredTweet)['compound']
            newObj = SentenceWithSentiment(alteredTweet, sentimentOfNewString, htmlText)
            listOfSentencesWithSentiments.append(newObj)
            
            if(sentimentOfNewString >= bestSentiment):
                bestSentiment = sentimentOfNewString
                bestSentimentString = htmlText;
            elif(sentimentOfNewString < worstSentiment):
                worstSentiment = sentimentOfNewString
                worstSentimentString = htmlText;
                
            
            if(sentimentOfNewString == mainSentiment or sentimentOfNewString == 0.0):
                if(PRINT_ALL_STRINGS and numberOfPrints <= SHOW_ALTS): displayText("{0}: {1}".format(htmlText,sentimentOfNewString),'black')
                numberOfPrints+=1;
            elif(sentimentOfNewString > mainSentiment):
                if(PRINT_ALL_STRINGS and numberOfPrints <= SHOW_ALTS): displayText("{0}: {1}".format(htmlText,sentimentOfNewString),'green')
                numberOfPrints+=1;
            elif(sentimentOfNewString < mainSentiment and sentimentOfNewString != 0.0):
                if(PRINT_ALL_STRINGS and numberOfPrints <= SHOW_ALTS): displayText("{0}: {1}".format(htmlText,sentimentOfNewString),'red')
                numberOfPrints+=1;
                
    if(numberOfPrints > SHOW_ALTS): print("--- More options (total: {0}) possible, but not printed ---".format(numberOfPrints));
    if (worstSentimentString != ""): displayText("Worst Sentence: {0} : {1}".format(worstSentimentString, worstSentiment), color='red')
    if (bestSentimentString != ""): displayText("Best Sentence: {0} : {1}".format(bestSentimentString, bestSentiment), color='green') 
    
    
    sentenceObj.resetFinalSentences();
    sentenceObj.addFinalSentences(listOfSentencesWithSentiments)
    return listOfSentencesWithSentiments;


def getHTMLPage():
    global RETURN_HTML_REPLACEMENT; 
    bigPage = ''
    bigPage += ' <ul>'
    for html in RETURN_HTML_REPLACEMENT:
        if("Tweet: " in html):
            bigPage += "</ul>  <br/> <ul> "
        bigPage += "<li> {0} </li>".format(html);
    bigPage += '</ul>'
    return bigPage


def cstr(s, color='black', italics=False):
    if(COLOR_PRINTING):
        if(italics):
            return cstr("<i>{0}</i>".format(s), color);
        return "<text style=color:{}>{}</text>".format(color, s)
    else:
        return "{}".format(s)

def displayText(text, color='black'):
    if(COLOR_PRINTING):
        if(__name__== "__main__"):
            RETURN_HTML_REPLACEMENT.append((cstr(text, color)))
            return
        display(HTML(cstr(text, color)));
        return
    print("{}".format(text));
    
    
def cleanAndTokenizeText(text):
    text = text.lower();
    newString = ""
    for char in text:
        if char not in punctuation:
            newString += char
    text = word_tokenize(newString)
    return text;

def getPOSTags(tweet):
    if(USE_SPACY == False):
        tags = nltk.pos_tag(tweet)
        return tags;    
    tweet = ' '.join(tweet)
    doc = nlp(tweet)
    tags = [(token.text, token.tag_) for token in doc] # since the format expected is [text,tag]
    return tags

def getAntonymsOfWords(word):
    if(word not in vocabulary):
        return []
    setOfAntonyms = set()
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            anton = l.antonyms()
            if(anton!=[]):
                setOfAntonyms.add(anton[0].name())
    if(len(setOfAntonyms) == 0):
        if(VERBOSE_PRINTING): print("No antonyms found for word {0}".format(word))
    return list(setOfAntonyms)

def returnReplacementsForWord(word):
    
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
    
def generateHTMLObjectsFromSentence(sentenceObj):
    
    allSentences = sentenceObj.getFinalSentences()
    indexToAlts = sentenceObj.indexToSetOfWords;
    indexToChange = list(indexToAlts.keys());
    
    listOfSentenceObjs = []
    for sentence in allSentences:
        copySentence = cleanAndTokenizeText(sentence)
        for index in indexToChange:
            copySentence[index] = cstr("[{0}]".format(copySentence[index]), "blue", italics=True);
        listOfSentenceObjs.append(SentenceWithHTML(sentence, ' '.join(copySentence)));
    
    return listOfSentenceObjs
    

def helper_combine(mainList, myList):
    '''
    helper function for CombineSentenceChunks
    '''
    newList = []
    for val in myList:
        for mainVal in mainList:
            # if(VERBOSE_PRINTING): print("Combining {0} with {1}".format(' '.join(val), ' '.join(mainVal)));
            newList.append(val + mainVal);
    return newList;

def combineSentenceChunks(wholeSentence, dictOfChunks):
    '''
        Uses the helper_combine function to generate all possible combinatios and permuations of the chunks
        and any alternatives.
        
        The logic is to use the end of the sentence, apply each possible chunk from the previous key's chunks
        to every possible chunk of this key's.
        
        The helper function is used to allow us to reuse the list of alreadyGeneratedChunks and constantly
        append to them.
        
        To understand the logic better, take a look at this gist:
        https://gist.github.com/sunnyMiglani/cf85407a9e6928237b1436cc2bc95fa4
        
    '''
    reversedKeys = sorted(dictOfChunks.keys(), reverse=True)
    completeSentences = [];
    mainArr = dictOfChunks[reversedKeys[0]]
    for ind in range(1, len(reversedKeys)):
        key = reversedKeys[ind];
        mainArr = helper_combine(mainArr, dictOfChunks[key]);
        
    return mainArr;
        
def generateSentenceChunks(wholeSentence, keyToChange, nextKey, listOfMyAlternatives):
    '''
        Generates sentence chunks by iterating through the list of alternatives
        Chunking the sentence to start from current key to next key.
        This means that the sentence always goes from key 'x' to key 'y'
        
        Example:
        "I really <hate> hot chocolate, but I <prefer> hot coffee"
        Calling generateSentenceChunks will create an example sentence:
            - "<altWordForHate> hot chocolate , but I "
        
        Remember to append the first stretch of the string to the first key's chunk for proper use!
    '''
    newList = list(listOfMyAlternatives)
    newList.append(wholeSentence[keyToChange]);
    generatedSentences = []
    for myAlt in newList:
        newSentence = wholeSentence[:]
        newSentence[keyToChange] = myAlt
        if(VERBOSE_PRINTING): print("Generated : {}".format(newSentence[keyToChange:nextKey]))
        generatedSentences.append(newSentence[keyToChange:nextKey]);
        
    return generatedSentences
    
def returnCombinationsOfStrings(sentenceObj):
    
    indexToWordDict = sentenceObj.indexToSetOfWords;
    originalSentence = sentenceObj.ogSentence;
    tokenizedSentence = cleanAndTokenizeText(originalSentence)
    reversedKeys = sorted(indexToWordDict.keys(), reverse=True)
    dictAlternatives  = {}

    sortedKeys = sorted(indexToWordDict.keys())
    sentenceChunks = {}
    htmlChunks = {}
    
    for ind in range(0,len(sortedKeys)):
        key = sortedKeys[ind]
        nextKey = sortedKeys[ind+1] if ind+1 < len(sortedKeys) else len(tokenizedSentence)
        sentenceChunks[key] = generateSentenceChunks(tokenizedSentence, key, nextKey, indexToWordDict[key])

    if(sortedKeys[0] != 0):
        newList = []
        for thislist in sentenceChunks[sortedKeys[0]]:
            newList.append(tokenizedSentence[0:sortedKeys[0]] + thislist)
        sentenceChunks[sortedKeys[0]] = newList;
        
    finalOptions = combineSentenceChunks(tokenizedSentence, sentenceChunks)
    
    finalSentences = []
    for val in finalOptions:
        sentence = ' '.join(val)
        finalSentences.append(sentence)
    
    sentenceObj.resetFinalSentences()
    sentenceObj.addFinalSentences(finalSentences)   
    return sentenceObj


# In[22]:


def getAlternativeSentences(sentenceObj):
    mainSentence = sentenceObj.ogSentence;
    mainSentiment = sentenceObj.ogSentiment;

    sentenceTokens = cleanAndTokenizeText(mainSentence)

    for ind, word in enumerate(sentenceTokens):
        alternativeSentenceWithHTML = []
        copyOfTokens = sentenceTokens[:]
        replacements = []
        
        score = senty.polarity_scores(word)['compound']
        if(score != 0.0):
            tempReplacements = returnReplacementsForWord(word) # get embedding based relations
            if(tempReplacements == []):
                print("No replacements found at all for word {0}".format(word))
                continue
            replacements = posApprovedReplacements(tempReplacements[:], copyOfTokens[:], ind)
            finalReplacements = []
            if(VERBOSE_PRINTING): skippedWords = []
            for word in replacements:
                thisSentiment = senty.polarity_scores(word)['compound']
                if(thisSentiment != 0.0):
                    finalReplacements.append(word)
                else:
                    if(VERBOSE_PRINTING):
#                         print("Sentiment of Skipped word {} is {}".format(word, senty.polarity_scores(word)))
                        skippedWords.append(word)
            if(VERBOSE_PRINTING and len(skippedWords) > 0):
                print("some skipped words: {0}".format(skippedWords[:5]));
            if(finalReplacements == []):
                if(VERBOSE_PRINTING): print(" -- No POS approved words! -- for word {0}\n some non-POS:{1}".format(word, tempReplacements[:4]))
                continue
            sentenceObj.addAlternativesByIndex(ind, finalReplacements)
    return sentenceObj



def interactionHelper(dictOfAltObjs, sentiments, thisSent, lastWorkingIndex=0):
    if(thisSent in sentiments):
        mainIndex = sentiments.index(thisSent)
        
    else:
        mainIndex = lastWorkingIndex
    
    numLower =  mainIndex  # Mod to keep it in range 0 -> val 
    numHigher = len(sentiments) - mainIndex - 1

    print("There are totally {0} possible sentences".format(len(sentiments)))
    print("Current sentiment is at index {0}, and length of sentiments is {1}".format(mainIndex, len(sentiments)));
    print(" <--- {0} lower and {1} ---> higher ".format(numLower, numHigher))
    print("Would you like to see a lower sentiment or higher sentiment or ALL?")
    print("Please enter 1 for lower, 2 for higher or 0 for all")
    
    targetSentiment = thisSent
    textInput = input()
    if(textInput == ""):
        print("You entered nothing! exiting")
        return
        
    if(textInput.isdigit()):
        textInput = int(textInput)
        if(textInput == 0):
            if(VERBOSE_PRINTING): print("Printing sentiments from : {0}".format(sentiments))
            for sentiment in sentiments:
                obj = dictOfAltObjs[sentiment][0];
                displayText("{0}  : {1}".format(obj.getHTML(), sentiment))
            return
        elif(textInput == 1 and numLower > 0 and (mainIndex - 1) >= 0):
            targetSentiment = sentiments[mainIndex - 1]
            htmlSentence = dictOfAltObjs[targetSentiment][0].getHTML();
            displayText("{0} : {1}".format(htmlSentence, targetSentiment))
            
        elif(textInput == 2 and numHigher < len(sentiments) and (mainIndex + 1) < len(sentiments)):
            targetSentiment = sentiments[mainIndex + 1]
            htmlSentence = dictOfAltObjs[targetSentiment][0].getHTML();
            displayText("{0} : {1}".format(htmlSentence, targetSentiment))
            
        else:
            print("You entered an invalid option")
            interactionHelper(dictOfAltObjs, sentiments, thisSent, mainIndex)
            return
        
    interactionHelper(dictOfAltObjs, sentiments, targetSentiment,mainIndex)



def interactionWithUser(mainSentenceObj, dictOfAltObjs,sentiments, isUser=False):
    if(isUser == False):
        return
    else:
        mainSentence = mainSentenceObj.ogSentence;
        mainSent = mainSentenceObj.ogSentiment;
        if(VERBOSE_PRINTING):
            print("The following are the sentiment values for the input")
            for ind,sent in enumerate(sentiments):
                print("{0} - {1}".format(ind+1,sent))
        
        interactionHelper(dictOfAltObjs, sentiments, mainSent) 


def extractTwitterDataset():
    df_tweets = pd.read_csv( pathToDatasets + 'cleanedTweets.csv', nrows=NUM_OF_TWEETS, skiprows =TWEET_START)
    tweets = df_tweets.values
    return tweets;

def createDictionaryOfSentStrings(sentencesWithSentiment):
    dict_sentimentToStringObjects = {}
    for obj in sentencesWithSentiment:
        sent = obj.getSentiment()
        if(dict_sentimentToStringObjects.get(sent) == None):
            dict_sentimentToStringObjects[sent] = [obj]
        else:
            (dict_sentimentToStringObjects[sent]).append(obj)

    return dict_sentimentToStringObjects;

def runThroughTweets():
    tweets = extractTwitterDataset()
    if(RUN_AS_MAIN):
        global RETURN_HTML_REPLACEMENT;


    counterOfTweets = 0;
    for counter,tweet in enumerate(tweets):
        counterOfTweets +=1;
        tweet = tweet[0]
        tweetTokens = cleanAndTokenizeText(tweet)
        mainSentiment = senty.polarity_scores(tweet)['compound']
        if(mainSentiment == 0):
            continue
        if(RUN_AS_MAIN):
            RETURN_HTML_REPLACEMENT.append("\n\n Tweet: {0}:{1}\n".format(tweet,mainSentiment))  
        else:
            print("\n\n Tweet: {0}:{1}\n".format(tweet,mainSentiment)) 

        sentenceObj = Sentence(tweet, mainSentiment)
        sentenceObj = getAlternativeSentences(sentenceObj)
        replacementDictionary = sentenceObj.getDictOfIndexWords();
        if(len(replacementDictionary) <= 0):        
            print(" -- No new Strings generated ---\n\n")
            continue

        keysToChange = replacementDictionary.keys();
        for key in keysToChange:
            if(VERBOSE_PRINTING):print("{0}'th word's ({2}) options: {1}".format(key,replacementDictionary[key],tweetTokens[key]))

        sentenceObj = returnCombinationsOfStrings(sentenceObj)
        sentencesWithSentiment = printStrings(sentenceObj)

        dict_sentimentToStringObjects = createDictionaryOfSentStrings(sentencesWithSentiment)
        
        sentiments = sorted(dict_sentimentToStringObjects.keys())
        if(VERBOSE_PRINTING):print("sentiments:{0}".format(sentiments))

    return getAllHTML;
        
    return counterOfTweets;


# In[26]:


specificString = ""
def specificString(textString=""):
    if(textString == "" or textString == None):
        return
    textString = dataClean(textString)
    mainSentiment = senty.polarity_scores(textString)['compound']
    if(mainSentiment == 0):
        print("{} \n No sentiment found in sentence".format(textString));
        if(RUN_AS_MAIN):
            RETURN_HTML_REPLACEMENT.append("{} \n No sentiment found in sentence".format(textString))
        return;
    print("\n {0}:{1}\n".format(textString,mainSentiment))   
    sentenceObj = Sentence(textString, mainSentiment)
    sentenceObj = getAlternativeSentences(sentenceObj)
    replacementDictionary = sentenceObj.getDictOfIndexWords();
    if(len(replacementDictionary) <= 0):        
        print(" -- No new Strings generated ---\n\n")
        if(RUN_AS_MAIN):
            RETURN_HTML_REPLACEMENT.append(" -- No new Strings generated ---")
        return
    
    keysToChange = replacementDictionary.keys();
    if(VERBOSE_PRINTING):
        for key in keysToChange:
            print("{0}'th word's options: {1}".format(key,replacementDictionary[key]))
        
    sentenceObj = returnCombinationsOfStrings(sentenceObj)
    allPossibleSentences = printStrings(sentenceObj)
    
    
    dict_sentimentToStringObjects = createDictionaryOfSentStrings(allPossibleSentences)    

    sentiments = sorted(dict_sentimentToStringObjects.keys())
    interactionWithUser(sentenceObj, dict_sentimentToStringObjects, sentiments[0:10], False);
    return  allPossibleSentences


if (RUN_AS_MAIN):
    print("You've run this file as a main file!")
    print("This should now run a web server!")

@app.route('/view-all')
def routerViewAll():
    htmlPageReturned = runThroughTweets()
    return htmlPageReturned

@app.route('/view-all/<int:start>/<int:number>')
def routerViewTweets(start, number):
    global TWEET_START
    global NUM_OF_TWEETS 
    oldStart = TWEET_START;
    oldNum = NUM_OF_TWEETS;

    TWEET_START = start
    NUM_OF_TWEETS = number
    
    htmlPageReturned = runThroughTweets()

    TWEET_START = oldStart
    NUM_OF_TWEETS = oldNum
    

    return htmlPageReturned

@app.route('/user/<string:userString>')
def userStringTest(userString):
    allPossible =  specificString(userString)
    result = []
    obj = {}
    return render_template("big_display.html", listOfObjs=result)

@app.route('/user_entry')
def userInteract():
    return '''
    <html>
    <body>

        <h2>HTML Forms</h2>
        <form action="/">
        Last name:<br>
        <input type="text" name="lastname" value="Mouse">
        <br><br>
        <input type="submit" value="Submit">
        </form> 

        <p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>

        </body>
    </html>

    
    '''

@app.route('/')
def introFunction():
    return render_template("index.html")

if(RUN_AS_MAIN):
    print("Going to now run the app!");
    app.run(host=  '0.0.0.0', port=5000, debug=True)
