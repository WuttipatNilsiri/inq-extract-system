import pandas as pd
import os

import sys

train_data = sys.argv[1]
model_path = sys.argv[2]

dataset = pd.read_csv(train_data, encoding='ISO-8859-1')

import re
import nltk

import pickle

import wordlist as wl

nltk.download('punkt')
from nltk.tokenize import word_tokenize as wt 

# nltk.download('stopwords')
# from nltk.corpus import stopwords

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

#spell correction
from autocorrect import spell

data = []

doNOT = wl.doNOT

stopword = wl.stopword

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


for i in range(dataset.shape[0]):
    
    
    sms = dataset.iloc[i, 1]

    # remove non alphabatic characters
    data.append(process(sms))

# print(data[12])

from sklearn.feature_extraction.text import CountVectorizer
matrix = CountVectorizer(max_features=1000)
fittedMatrix = matrix.fit_transform(data)

with open(model_path + '\\matrix.model', 'wb') as fid:
    pickle.dump(matrix, fid)

X = fittedMatrix.toarray()
# print(array(X[0],X[1]))


y = dataset.iloc[:, 0]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

with open(model_path + '\\classifier.model', 'wb') as fid:
    pickle.dump(classifier, fid)



# predict class
y_pred = classifier.predict(X_test)
print(y_pred)

# Confusion matrix
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
# cm = confusion_matrix(y_test, y_pred)
# cr = classification_report(y_test, y_pred)

accuracy = accuracy_score(y_test, y_pred)
print("accuracy: " + str(accuracy))