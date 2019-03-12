import SentenceClasses

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

def cstr(s, color='black', italics=False):
    if(COLOR_PRINTING):
        if(italics):
            return cstr("<i>{0}</i>".format(s), color);
        return "<text style=color:{}>{}</text>".format(color, s)
    else:
        return "{}".format(s)

def displayText(text, color='black'):
    if(COLOR_PRINTING):
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

if(__name__ == "__main__"):
    print("CAUTION: You're running the shifting code library alone, this will cause errors")
else:
    print("Imported SentimentShifting Library");