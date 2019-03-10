
# coding: utf-8

# ## Import Statements

# In[1]:


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

from flask import Flask
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
app = Flask(__name__)

sys.path.insert(0, pathToDataScripts)
# from cleanDataset import tokenize_words


from IPython.core.display import display, HTML
# display(HTML("<style>.container { width:85% !important; }</style>"))


# ## Downloading binaries and models
#

# In[2]:


print("Should I reload the model?")
tstString = input()
if("no" in tstString.lower()):
    print(" didnt reload model! ")
else:
    print("Am loading the model!");
    word_vectors = api.load("glove-wiki-gigaword-100")
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

print("Finished the model section")
# ## Global Variables and Global Objects

# In[3]:


senty = SentimentIntensityAnalyzer()
vocabulary = word_vectors.vocab;

nlp = spacy.load('en')


NUMBER_OF_ALTERNATIVES = 5
TWEET_START = 100
NUM_OF_TWEETS = 50


VERBOSE_PRINTING = True
# VERBOSE_PRINTING = False

USE_SPACY = False
# USE_SPACY = True


punctuation = r"\"#$%&'+-/;<=>?@[\]*^_`{|}~"


# ## Class for Sentences
#

# In[4]:


class SentenceWithHTML():

    def __init__(self,sentence,html):
        self.sentence = sentence;
        self.html = html;

    def getHTML(self):
        return self.html;

    def getSentence(self):
        return self.sentence

    def setHTML(self, html):
        self.html = html;

    def setSentence(self, sentence):
        self.sentence = sentence


class Sentence:


    def __init__(self, sentence, sentiment):
        self.ogSentence = sentence;
        self.ogSentiment = sentiment;
        self.indexToSetOfWords = {}
        self.alternateSentences = [];
        self.finalShiftSentences = [];

    def addAlternativesByIndex(self, index, listOfAlternatives):
        '''
            Adds the list of possible alternative words that
            can be used per word based on the index of the word in the tokenized
            sentence. (from cleanAndTokenizeText())
        '''
        if(self.indexToSetOfWords.get(index)):
            self.indexToSetOfWords[index] = self.indexToSetOfWords.union(set(listOfAlternatives))
        else:
            self.indexToSetOfWords[index] = set(listOfAlternatives)

    def addAlternativeStrings(self, strings):
        if(isinstance(strings,str)):
            self.alternateStrings = list(set(self.alternateStrings.append(strings)))
            self.alternateSentences.append(strings)
        else:
            self.alternateSentences.extend(strings)



    def addFinalSentences(self, sentences):
        if(isinstance(sentences, str)):
            self.finalShiftSentences.append(sentences)
        else:
            self.finalShiftSentences.extend(sentences)

    def resetFinalSentences(self):
        self.finalShiftSentences = [];




# ## Utility Code

# In[5]:


def cstr(s, color='black', italics=False):
    # if(italics):
        # return cstr("<i>[{0}]</i>".format(s), color);
    # return "<text style=color:{}>{}</text>".format(color, s)
    return "{}".format(s)

def displayText(text, color='black'):
    # display(HTML(cstr(text, color)));
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
    tags = [(token.text, token.pos_) for token in doc] # since the format expected is [text,tag]
    return tags;


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


# In[6]:


def printStrings(sentenceObj):
    newStrings = sentenceObj.finalShiftSentences;
    mainSentiment = sentenceObj.ogSentiment;
    for ind, tSentence in enumerate(newStrings):
            alteredTweet = tSentence.getSentence()
            htmlText = tSentence.getHTML()
            sentimentOfNewString = senty.polarity_scores(alteredTweet)['compound']
            if(sentimentOfNewString == mainSentiment or sentimentOfNewString == 0):
                displayText("{0}: {1}".format(htmlText,sentimentOfNewString), 'DarkGray');
            elif(sentimentOfNewString > mainSentiment):
                displayText("{0}: {1}".format(htmlText,sentimentOfNewString),'green')
            else:
                displayText("{0}: {1}".format(htmlText,sentimentOfNewString),'red')


# In[7]:


def runThroughExampleTweets():

    tweets_df = pd.read_csv( pathToDatasets + 'cleanedTweets.csv' , nrows=NUM_OF_TWEETS, skiprows=TWEET_START)

    tweets = tweets_df.values

    listOfObjects = []
    for counter,tweet in enumerate(tweets):
        tweet = tweet[0]
        mainSentiment = senty.polarity_scores(tweet)['compound']
        if(mainSentiment == 0):
            continue
        print("\n {0}:{1}\n".format(tweet,mainSentiment))
        sentenceObj = Sentence(tweet, mainSentiment)
        sentenceObj = getAlternativeSentences(sentenceObj)
        alternateTweets = (sentenceObj.alternateSentences)[:]
        if(alternateTweets == [] or alternateTweets == None):
            print(" -- No new Strings generated ---\n\n")
            continue
        sentenceObj = shiftSentiment(sentenceObj, True);
        printStrings(sentenceObj)
        sentenceObj = shiftSentiment(sentenceObj, False);
        printStrings(sentenceObj)



# ## Testing Code
#

# In[8]:


specificWord = "good"
def testOneWord(word=""):
    if(word==""):
        return
    print(word)


# ## Main Cell
#

# In[9]:


specificString = ""
def specificString(textString=""):
    if(textString == "" or textString == None):
        return
    mainSentiment = senty.polarity_scores(textString)['compound']
    if(mainSentiment == 0):
        print("{} \n No sentiment found in sentence".format(textString));
        return;
    print("\n {0}:{1}\n".format(textString,mainSentiment))
    sentenceObj = Sentence(textString, mainSentiment)
    sentenceObj = getAlternativeSentences(sentenceObj)
    alternateTweets = (sentenceObj.alternateSentences)[:]
    if(alternateTweets == [] or alternateTweets == None):
        print(" -- No new Strings generated ---\n\n")
        return
    sentenceObj = shiftSentiment(sentenceObj, True);
    printStrings(sentenceObj)
    sentenceObj = shiftSentiment(sentenceObj, False);
    printStrings(sentenceObj)

def welcomeInteraction():


    global VERBOSE_PRINTING
    global NUM_OF_TWEETS
    global TWEET_START
    VERBOSE_PRINTING = False;
    NUM_OF_TWEETS = 10;
    TWEET_START += 10;

    print("Welcome to the Sentimentally example!");
    print("You can see some example tweets in this code! or\nyou can enter your own!")
    print("Input '1' to see example tweets, or '2' to put your own or 3 to stop")
    choice = input()
    if('1' in choice or 'one' in choice):
        runThroughExampleTweets();
    elif('3' in input()):
        print("Goodbye!")
    else:
        print("You've chosen to input your own string!")
        print("Please enter the string below");
        inputString = input()
        if(inputString == ""):
            print("You're bad for trying to break this program, go away")
        else:
            specificString(inputString);
    welcomeInteraction()

@app.route('/test/<string>')
def specificStringWrapper(string):
    return specificString(string)

@app.route('/')
def hello_world():
    return ("hello world")
