
import client
import json

import database

import random 


email = client.Email()

ask_list = [
    'Can we have {} ?',
    'What is {} ?',
    'Can you provide the information(s) of {} ?'
]

# def send_init_mail(_id,_data):
#     email.send("me",_data.sender,"We recieve your inquiry ID: " + str(_id) , json.dumps(_data.toJSON(), indent=2))

def send_init_mail_doc(doc):
    _id = str(doc['_id'])
    del doc['_id']
    email.send("me",doc['Sender'],"We recieve your inquiry ID: " + str(_id) , json.dumps(doc, indent=2))
    

# def send_miss_mail(_id,_data,miss_list):
#     string_param = ','.join(miss_list)
#     ask_sentence = random.choice(ask_list) 
#     email.send("me",_data.sender,"Miss some information RE:<{}>".format(_id),'inquiry: ' + _data.sent+'\n'+ask_sentence.format(string_param))

def send_miss_mail_doc(doc,miss_list):
    _id = str(doc['_id'])
    del doc['_id']
    string_param = ','.join(miss_list)
    ask_sentence = random.choice(ask_list) 
    email.send("me",doc['Sender'],"Miss some information RE:<{}>".format(_id), json.dumps(doc, indent=2) +'\n'+ask_sentence.format(string_param))

def send_update_mail(doc):
    _id = str(doc['_id'])
    del doc['_id']
    email.send("me",doc['Sender'],"Notify Status of Inquiry ID: " + _id , json.dumps(doc, indent=2) +'\n'+"Status Inquiry: " + doc['Status'])


def readmail():
    return email.read()
