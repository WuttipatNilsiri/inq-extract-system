import threading
import client

from data import Data

import database

import ai

import bot

import until

import json

def reinq_process(_id,_data):
    doc = database.searchbyID(_id)
    category = doc['Category']
    print(category)
    param_list = ai.extract(category,_data.sent.split(' On')[0])
    print(param_list)
    param_json = doc['Param_list']
    for x in param_list:
        param_json[x[0]] = x[1]
    miss_list = until.validateParam(category,param_json)
    database.update(_id,{"Param_list" : param_json})
    if len(miss_list) == 0:
        bot.send_init_mail_doc(database.searchbyID(_id))
    else:
        bot.send_miss_mail_doc(database.searchbyID(_id),miss_list)

def save2DB(_data):
    miss_list = _data.validateParam()
    valid_data = _data.toJSON()
    print(json.dumps(valid_data, indent=2))
    _id = database.save(valid_data)
    
    if len(miss_list) == 0:
        return (_id , [])
    else:
        return (_id , miss_list)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t



def loop():
    res = bot.readmail()
    print(res)
    print ("Total messaged retrived: ", str(len(res)))
    
    if len(res) > 0:
        for mess in res:

            _data = Data(mess)
            _id = _data.isREinq()

            if _id:
                reinq_process(_id,_data)
                continue

            category = ai.classify(_data.sent)
            print(category)

            _data.category = category

            param_list = ai.extract(category,_data.sent)
            
            _data.add_param_list(param_list)

            _id , miss_list = save2DB(_data)
            if _id and len(miss_list) == 0:
                bot.send_init_mail_doc(database.searchbyID(_id))
            else:
                bot.send_miss_mail_doc(database.searchbyID(_id),miss_list)

                

t = set_interval(loop,3)
