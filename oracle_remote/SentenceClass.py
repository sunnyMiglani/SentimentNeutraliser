import copy

class SentenceWithHTML():
    
    def __init__(self,sentence,html, sentiment=""):
        self.sentence = sentence;
        self.html = html;
        if(sentiment!=""):
            self.sentiment = sentiment;
        
    
    def getHTML(self):
        return self.html;
    
    def getSentence(self):
        return self.sentence
    
    def setHTML(self, html):
        self.html = html;
    
    def setSentence(self, sentence):
        self.sentence = sentence
    
    def setSentiment(self, sentiment):
        self.sentiment = sentiment;
       
    def getSentiment(self):
        return self.sentiment;
    
    def __str__(self):
        return "sentence : {0}".format(self.sentence)
        
class SentenceWithSentiment():
    
    def __init__(self, sentence, sentiment=-10 , html="No HTML"):
        self.sentence = sentence;
        self.sentiment = sentiment;
        self.html = html;
        self.sentenceTokens = []
      
    def getSentence(self):
        return self.sentence;
    
    def getSentiment(self):
        return self.sentiment;
    
    def getHTML(self):
        return self.html;
    
    def __str__(self):
        if(self.sentiment==-10):
            return "{0}".format(self.sentence)
        if(self.html == "No HTML"):
            return "{0} : {1}".format(self.sentence, self.sentiment)
        else:
            return "{0} : {1}".format(self.html, self.sentiment)
    
    def getSentenceTokens(self):
        return self.sentenceTokens[:]
    
    def setSentenceTokens(self, sentenceTokens):
        self.sentenceTokens = sentenceTokens;
        return

class Sentence:
    
    
    def __init__(self, sentence, sentiment):
        self.ogSentence = sentence;
        self.ogSentiment = sentiment;
        self.indexToSetOfWords = {};
        self.wordToAlternatives = {};
        self.finalShiftSentences = [];
        self.replacementsExist = False;
        self.sentenceTokens = [];

    def addAlternativesByIndex(self, index, listOfAlternatives):
        '''
            Adds the list of possible alternative words that 
            can be used per word based on the index of the word in the tokenized 
            sentence. (from cleanAndTokenizeText())
        '''
        if(self.indexToSetOfWords.get(index)):
            self.indexToSetOfWords[index] = self.indexToSetOfWords[index].union(set(listOfAlternatives))
        else:
            self.indexToSetOfWords[index] = set(listOfAlternatives)
    
    def addWordToAlternatives(self, word, listOfAlternatives):
        if(self.wordToAlternatives.get(word)):
            self.wordToAlternatives[word] = self.wordToAlternatives[word].union(set(listOfAlternatives))
        else:
            self.wordToAlternatives[word] = set(listOfAlternatives)
    
    
    def addFinalSentences(self, sentences):
        if(isinstance(sentences, str)):
            self.finalShiftSentences.append(sentences)
        else:
            self.finalShiftSentences.extend(sentences)
    
    def checkIfWordExists(self, word):
        if(self.wordToAlternatives.get(word)):
            return list(self.wordToAlternatives.get(word))
        else:
            return []
            
    def resetFinalSentences(self):
        self.finalShiftSentences = [];
        
    def getFinalSentences(self):
        return self.finalShiftSentences[:];
    
    def getDictOfIndexWords(self):
        return copy.copy(dict(self.indexToSetOfWords))
    
    def getDictOfWordsToAlternatives(self):
        return copy.copy(dict(self.wordToAlternatives))
    
    def getSentenceTokens(self):
        return self.sentenceTokens[:]
    
    def setSentenceTokens(self, sentenceTokens):
        self.sentenceTokens = sentenceTokens;
        return
       
            
if(__name__ == "__main__"):
	print("Running class file as main!");
else:
	print("Imported class file!");
