
import predict_classify
import predict_extract

import until

classifier = predict_classify.Classify()
extract_askinfo = predict_extract.Extractor("./extract-data/model/askinfo.model")
extract_req = predict_extract.Extractor('./extract-data/model/req.model')
extract_delay = predict_extract.Extractor('./extract-data/model/delay.model')

def classify(sent):
    return classifier.predict(sent)[0]
    
def extract(category,sent):
    _list_sent = sent.split(" ")
            
    label = []

    if category == 'askinfo':
                
                label = extract_askinfo.predict(sent)
            
    elif category == 'req' or category == 'request':
                
                label = extract_req.predict(sent)
                
    elif category == 'delay':
                
                label = extract_delay.predict(sent)

    param_list = until.getwordsbylabel(_list_sent,label)
    
    return param_list