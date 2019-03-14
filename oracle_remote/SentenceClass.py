import copy

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
    
    def __str__(self):
        return "sentence : {0}".format(self.sentence)
        
class SentenceWithSentiment():
    
    def __init__(self,sentence,sentiment, html="No HTML"):
        self.sentence = sentence;
        self.sentiment = sentiment;
        self.html = html;
      
    def getSentence(self):
        return self.sentence;
    
    def getSentiment(self):
        return self.sentiment;
    
    def getHTML(self):
        return self.html;
    
    def __str__(self):
        if(self.html == "No HTML"):
            return "{0} : {1}".format(self.sentence, self.sentiment)
        else:
            return "{0} : {1}".format(self.html, self.sentiment)

class Sentence:
    
    
    def __init__(self, sentence, sentiment):
        self.ogSentence = sentence;
        self.ogSentiment = sentiment;
        self.indexToSetOfWords = {}
        self.finalShiftSentences = [];
        self.replacementsExist = False;

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
    
    
    def addFinalSentences(self, sentences):
        if(isinstance(sentences, str)):
            self.finalShiftSentences.append(sentences)
        else:
            self.finalShiftSentences.extend(sentences)

    def resetFinalSentences(self):
        self.finalShiftSentences = [];
        
    def getFinalSentences(self):
        return self.finalShiftSentences[:];
    
    def getDictOfIndexWords(self):
        return copy.copy(dict(self.indexToSetOfWords))
            
if(__name__ == "__main__"):
	print("Running class file as main!");
else:
	print("Imported class file!");
