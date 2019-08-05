import pickle

import re
import nltk

import pickle

import wordlist as wl

# nltk.download('punkt')
from nltk.tokenize import word_tokenize as wt 

# nltk.download('stopwords')
from nltk.corpus import stopwords

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

#spell correction
from autocorrect import spell

import json

doNOT = wl.doNOT

stopword = wl.stopword

config = json.load(open('./config/config_classify.json'))

def process(sms):
    sms = re.sub('[^A-Za-z]', ' ', sms)

    # make words lowercase, because Go and go will be considered as two words
    sms = sms.lower()

    # tokenising
    tokenized_sms = wt(sms)
    print(tokenized_sms)

    # remove stop words and stemming
 
    sms_processed = []
    for word in tokenized_sms:
        if word not in set(stopword):
            if word in set(doNOT):
                word = "not"
            sms_processed.append(spell(stemmer.stem(word)))

    sms_text = " ".join(sms_processed)
    return sms_text

class Classify():
    
    matrix_file = open(config["matrix_model_path"], 'rb')
    classify_file = open(config["classify_model_path"], 'rb')
    
    def __init__(self):
        self.matrix = pickle.load(self.matrix_file)
        self.classifier = pickle.load(self.classify_file) 
    
    def predict(self,_input):
        x_test = self.matrix.transform([process(_input)]).toarray()
        print(x_test)
        y_pred = self.classifier.predict(x_test)
        # print(y_pred)
        return y_pred



# c = classify()
# res = c.predict("i want to know some information about promotion")
# print(res)


# sent = " i want to know some information about promotion"

# with open('./model/matrix.pkl', 'rb') as fid:
#     matrix = pickle.load(fid)
#     x_test = matrix.transform([process(sent)]).toarray()
#     print(x_test)

#     with open('./model/classifier.pkl', 'rb') as fid2:
#         classifier = pickle.load(fid2)  

#         y_pred = classifier.predict(x_test)
#         print(y_pred)


