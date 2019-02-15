import gensim
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim.downloader as api
import numpy as np

pathToDatasets = '../datasets/'
filePath = '../datasets/GoogleNews-vectors-negative300.bin'

word_vectors = api.load("glove-wiki-gigaword-100")

positiveWordList = ['affability', 'affable', 'affably', 'affectation', 'affection', 'affectionate', 'affinity', 'affirm', 'affirmation', 'affirmative']
negativeWordList = ['varice', 'avaricious', 'avariciously', 'avenge', 'averse', 'aversion', 'aweful', 'awful', 'awfully', 'awfulness']

dimensionsDictionary = {}
countOfWords = 0;

def countDimensions(listOfDimensions):
  for dimension in listOfDimensions:
    if (dimensionsDictionary.get(dimension) == None):
      dimensionsDictionary[dimension] = 1;
    else:
      dimensionsDictionary[dimension] +=1;


  
def sortedDictionary(dictUnsorted):
  sorted_d = sorted(dictUnsorted.items(), key=lambda x: x[1], reverse=True)
  return sorted_d;



rankDistance = word_vectors.rank("love", "hate")
print("Rank of hate in terms of distance from love is : {}".format(rankDistance));

wordVecLove = word_vectors.word_vec("love");
wordVecHate = word_vectors.word_vec("hate");

print("Word vectors for \nlove = {}\nhate={}".format(wordVecLove, wordVecHate));

differenceBetweenLoveHate = wordVecHate - wordVecLove
argMax = np.argmax(differenceBetweenLoveHate)
print("dimension of maxArg : {}".format(argMax));

vocabulary = word_vectors.vocab;
for posWord in positiveWordList:
  if(posWord not in vocabulary):
    continue  
  posVector = word_vectors.word_vec(posWord)
  for negWord in negativeWordList:
    if(negWord not in vocabulary):
      continue
    negVector = word_vectors.word_vec(negWord)
    diffBetween = posVector - negVector
    sortedList = sorted(range(len(diffBetween)), key=lambda k: diffBetween[k], reverse=True)
    similarityScore = word_vectors.similarity(posWord, negWord);
    print("Dimensions for word {0} and word {1} is {2} with similarity scores: {3}".format(posWord, negWord, sortedList[0:3], similarityScore))
    countDimensions(sortedList[0:3]);
    countOfWords+=1;
    # print("----- {} -----".format(diffBetween));

# print(dimensionsDictionary);
print(sortedDictionary(dimensionsDictionary));
print("Count of number of word pairs : {0}".format(countOfWords))

