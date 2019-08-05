from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite

from until import *

import sys

train_data = sys.argv[1]
outmodelfullpath = sys.argv[2]

def file2IOB(filename):
    FILE = open(filename,"r", encoding='ISO-8859-1', errors='ignore')
    listsent = []
    listword = []
    
    for line in FILE:
        
        if line and line != '\n' :
            if line.split(" ")[0] == '.':
                listsent.append(listword)
                listword = []
                 
            else:
                
                linesplited = line.rstrip().split(' ')
                listword.append(tuple(linesplited))
    FILE.close()
    return listsent

train_sents = file2IOB(train_data)

print(train_sents)
print(len(train_sents))

X_train = [sent2features(s) for s in train_sents]
# print(X_train)
y_train = [sent2labels(s) for s in train_sents]
# print(y_train)

# X_test = [sent2features(s) for s in test_sents]
# y_test = [sent2labels(s) for s in test_sents]
# print(sent2features(train_sents[0])[0])
# print(train_sents)
# print(test_sents)

trainer = pycrfsuite.Trainer(verbose=False)
for xseq, yseq in zip(X_train, y_train):
    trainer.append(xseq, yseq)


trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 50,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})


trainer.train(outmodelfullpath)
# trainerNLP.train('./model/engNLP.model')

# print(trainer.logparser.last_iteration)

# tagger = pycrfsuite.Tagger()
# tagger.open('engNER.model')

# example_sent = test_sents[1]
# print(example_sent)
# print(' '.join(sent2tokens(example_sent)), end='\n\n')

# print("Predicted:", ' '.join(tagger.tag(sent2features(example_sent))))
# print("Correct:  ", ' '.join(sent2labels(example_sent)))