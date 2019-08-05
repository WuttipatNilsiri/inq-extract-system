from autocorrect import spell

req = {
    "delay": ['ID','DATE','TYPE'],
    'request': [],
    'askinfo': []
}


def validateParam(cat,param_json):
        req_list = req[cat]
        miss_list = []
    
        if len(req_list) == 0:
            return miss_list

        for x in req_list:
            if x not in param_json.keys():
                miss_list.append(x)    
    
        return miss_list 

def autocorrectsent(sent):
    newsent = []
    for x in sent.split(' '):
        newsent.append(spell(x))
    return ' '.join(newsent)

def isSplitable(word,spliter):
    if (word.split(spliter)[0] == word):
        return False
    else:
        return True

def isAfterSplitedAllisDigit(word,spliter):
    for x in word.split(spliter):
        if not x.isdigit():
            return False
    
    return True

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        # 'word[-3:]=' + word[-3:],
        # 'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
        'isSplitable(word,"/")=%s' % isSplitable(word,"/"),
        'isAfterSplitedAllisDigit(word,"/")=%s' % isAfterSplitedAllisDigit(word,"/"),
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
    if i > 1:
        word1 = sent[i-2][0]
        postag1 = sent[i-2][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    if i < len(sent)-2:
        word1 = sent[i+2][0]
        postag1 = sent[i+2][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label_1 for token, postag, label_1 in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

def getwordsbylabel(sent,labels):
    # print(sent)
    res = []
    check = False
    labels.append("O")
    toappend = []
    toappend2 = []
    for i in range(len(labels)):
        if labels[i].split("-")[0] == "B" and not check:
            check = True
            _label = labels[i].split("-")[1]
            toappend.append(_label)
            toappend2.append(sent[i])
        elif labels[i].split("-")[0] == "I" and check:
            toappend2.append(sent[i])
        elif labels[i].split("-")[0] == "B" and check:
            if len(toappend) > 0:
                toappend.append(' '.join(toappend2))
                res.append(toappend)
            toappend = []
            toappend2 = []
            
            _label = labels[i].split("-")[1]
            toappend.append(_label)
            toappend2.append(sent[i])
        else:
            if len(toappend) > 0:
                toappend.append(' '.join(toappend2))
                res.append(toappend)
            check = False
            toappend = []
            toappend2 = []
    return res