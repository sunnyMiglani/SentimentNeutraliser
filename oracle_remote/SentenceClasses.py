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
        
if(__name__ == "__main__"):
    print("Running sentence class!")
else:
    print("Imported sentence class!")