import html.parser as htmlparser

import re

parser = htmlparser.HTMLParser()

req = {
    "delay": ['ID','DATE','TYPE'],
    'request': [],
    'askinfo': []
}

class Data():
    def __init__(self,mess):
        self.date = mess['Date']
        self.sent = parser.unescape(mess['Snippet'])
        self.sender = ""
        self.status = "processing"
        self.category = "NONE"
        self.subj = mess['Subject']
        try: 
            self.sender = re.search('<(.+?)>',mess['Sender']).group(1)
        except:
            self.sender = mess['Sender']
        self.param_json = {}

    def toJSON(self):
        data = {
            "Date" : self.date,
            "Subject" : self.subj,
            "Sender" : self.sender,
            "Sentence" : self.sent,
            "Category" : self.category,
            "Status" : self.status,
            "Param_list" : self.param_json
        }
        return data
    
    def add_param_list(self,param_list):
        for x in param_list:
            self.param_json[x[0]] = x[1]

    def validateParam(self):
        req_list = req[self.category]
        miss_list = []
    
        if len(req_list) == 0:
            return miss_list

        for x in req_list:
            if x not in self.param_json.keys():
                miss_list.append(x)    
    
        return miss_list 
    
    def isREinq(self):
        try:
            _id = re.search('RE:<(.+?)>',self.subj).group(1)
            print(_id)
            return _id
        except:
            return None