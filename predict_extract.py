from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite

from until import *

def loadlib():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

def merge(result,predicted):
    listres = []
    for i in range(len(result)):
        listx = list(result[i])
        listx[2] = predicted[i]
        listres.append(tuple(listx))
    return listres

class chucker():
    
    def word2IOB(self,word):
        text = nltk.word_tokenize(word)
        x = nltk.pos_tag(text)
        modified = [ele + ('X',) for ele in x]
        return modified
        
class Extractor():

    c = chucker()
    
    

    def __init__(self, model_path):
        self.model_path = model_path
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model_path)

        
    def predict(self,_input):
        # _input = autocorrectsent(_input)
        # print(_input)
        example_sent = self.c.word2IOB(_input)
        # print(example_sent)
        print(' '.join(sent2tokens(example_sent)), end='\n\n')
        predicted = self.tagger.tag(sent2features(example_sent))
        # print("Predicted:", ' '.join( predicted ))
        return predicted
    
    def plot(self,_input):
        example_sent = self.c.word2IOB(_input)
        predicted = self.tagger.tag(sent2features(example_sent))
        learned = merge(example_sent,predicted)
        nltk.chunk.conlltags2tree(learned).draw()


#"package 7798789765 was ship out 5 day ago by EMS but i don't recieve my package ."
# print(result)

    

#############################










#############################




# print(predicted)

# listres = []
# for i in range(len(result)):
#     listx = list(result[i])
#     listx[2] = predicted[i]
#     listres.append(tuple(listx))
# learned = merge(result,predicted)
# print(merge(result,predicted))








# nltk.chunk.conlltags2tree(learned).draw()
# print("Correct:  ", ' '.join(sent2labels(learned)))
# x = nltk.pos_tag(text)
# print(x)
# ex = Extractor("./extract-data/model/req.model")

# # def extractaskinfo(_input):
# #     res = ex.predict(_input)
# #     return res

# sent = "i want to see image of package 455646465"


# res = ex.predict(sent)
# print(res)

# x = getwordsbylabel(sent.split(" "),res)
# print(x)
# ex.plot("package 7798789765 was ship out 5 day ago by EMS but i don't recieve my package")