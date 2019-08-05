import sys
file_name=sys.argv[1]
import codecs
from nltk.tokenize import RegexpTokenizer
import glob
import nltk
import re

# nltk.download('averaged_perceptron_tagger')

data_not=[]
def Unique(p):
    text=re.sub("<[^>]*>","",p)
    text=re.sub("\[(.*?)\]","",text)
    text=re.sub("\[\/(.*?)\]","",text)
    if text not in data_not:
        data_not.append(text)
        return True
    else:
        return False

pattern = r'\[(.*?)\](.*?)\[\/(.*?)\]'
tokenizer = RegexpTokenizer(pattern)

def toolner_to_tag(text):
    text=text.strip()
    text=re.sub("<[^>]*>","",text)
    text=re.sub("(\[\/(.*?)\])","\\1***",text)
    text=re.sub("(\[\w+\])","***\\1",text)
    text2=[]
    for i in text.split('***'):
        if "[" in i:
            text2.append(i)
        else:
            text2.append("[word]"+i+"[/word]")
    text="".join(text2)
    return text.replace("[word][/word]","")

def text2conll2002(text,pos=True):

    text=toolner_to_tag(text) 
    text=text.replace("''",'"')
    text=text.replace("’",'"').replace("‘",'"')#.replace('"',"")
    tag=tokenizer.tokenize(text)
    j=0
    conll2002="" 
    for tagopen,text,tagclose in tag: 
        word_cut=nltk.word_tokenize(text) 
        i=0
        txt5=""
        while i < len(word_cut): 
            if word_cut[i]=="''" or word_cut[i]=='"':pass
            elif i==0 and tagopen!='word': 
                txt5+=word_cut[i]
                txt5+='\t'+'B-'+tagopen
            elif tagopen!='word':
                txt5+=word_cut[i]
                txt5+='\t'+'I-'+tagopen
            else: 
                txt5+=word_cut[i]
                txt5+='\t'+'O'
            txt5+='\n'
            #j+=1
            i+=1
        conll2002+=txt5
    if pos==False:
        return conll2002
    return postag(conll2002) 

# print(text2conll2002(t,pos=False))
def postag(text):
    listtxt=[i for i in text.split('\n') if i!='']
    list_word=[]
    for data in listtxt:
        list_word.append(data.split('\t')[0])
    #print(text)
    list_word=nltk.pos_tag(list_word)
    text=""
    i=0
    for data in listtxt:
        text+=data.split('\t')[0]+'\t'+list_word[i][1]+'\t'+data.split('\t')[1]+'\n'
        i+=1
    return text

def get_data(fileopen):
	
	with open(fileopen, 'r',encoding='ISO-8859-1') as f:
		lines = f.read().splitlines()
	return [a for a in lines if Unique(a)]

def alldata(lists):
    text=""
    for data in lists:
        text+=text2conll2002(data)
        text+='\n'
    return text

def alldata_list(lists):
    data_all=[]
    for data in lists:
        data_num=[]
        
        txt=text2conll2002(data,pos=True).split('\n') 
        for d in txt:
                tt=d.split('\t')
                if d!="":
                    if len(tt)==3:
                        data_num.append((tt[0],tt[1],tt[2]))
                    else:
                        data_num.append((tt[0],tt[1]))
            #print(data_num)
        data_all.append(data_num)
        
    #print(data_all)
    return data_all

def alldata_list_str(lists):
	string=""
	for data in lists:
		string1=""
		for j in data:
			string1+=j[0]+"	"+j[1]+"	"+j[2]+"\n"
		string1+="\n"
		string+=string1
	return string

def get_data_tag(listd):
	list_all=[]
	c=[]
	for i in listd:
		if i !='':
			c.append((i.split("\t")[0],i.split("\t")[1],i.split("\t")[2]))
		else:
			list_all.append(c)
			c=[]
	return list_all
def getall(lista):
    ll=[]
    for i in lista:
        o=True
        for j in ll:
            if re.sub("\[(.*?)\]","",i)==re.sub("\[(.*?)\]","",j):
                o=False
                break
        if o==True:
            ll.append(i)
    return ll

data1=getall(get_data(file_name))
datatofile=alldata_list(data1) 
with open(file_name.replace(".raw","")+"-pos.train","w",encoding='ISO-8859-1') as f:
    i=0
    while i<len(datatofile):
        for j in datatofile[i]:
            f.write(j[0]+" "+j[1]+" "+j[2]+"\n")
        if i+1<len(datatofile):
            f.write("\n")
        i+=1

# with open(file_name.replace(".raw","")+".train","w",encoding='ISO-8859-1') as f:
#     i=0
#     while i<len(datatofile):
#         for j in datatofile[i]:
#             f.write(j[0]+" "+j[2]+"\n")
#         if i+1<len(datatofile):
#             f.write("\n")
#         i+=1