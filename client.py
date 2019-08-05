'''
Reading GMAIL using Python
	- Abhishek Chhibber
'''

'''
This script does the following:
- Go to Gmal inbox
- Find and read all the unread messages
- Extract details (Date, Sender, Subject, Snippet, Body) and export them to a .csv file / DB
- Mark the messages as Read - so that they are not read again 
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv

from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode


class Email():

    
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read
        store = file.Storage('storage.json') 
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
    
    def read(self, user_id='me',label_list=['INBOX','UNREAD']):
        
        unread_msgs = self.service.users().messages().list(userId=user_id,labelIds=label_list).execute()
        if unread_msgs['resultSizeEstimate'] == 0:
          return []
        mssg_list = unread_msgs["messages"]
        # print ("Total unread messages in inbox: ", str(len(mssg_list)))
        final_list = [ ]
        
        for mssg in mssg_list:
            # print(mssg)
            temp_dict = {}
            m_id = mssg['id'] # get id of individual message
            message = self.service.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
            payld = message['payload'] # get payload of the message 
            headr = payld['headers'] # get header of the payload


            for one in headr: # getting the Subject
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass


            for two in headr: # getting the date
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))    
                    m_date = (date_parse.date())   
                    temp_dict['Date'] = str(m_date)
                else:
                    pass

            for three in headr: # getting the Sender
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass

            temp_dict['Snippet'] = message['snippet'] # fetching message snippet


            try:
		
		
                mssg_parts = payld['parts'] # fetching the message parts
                part_one  = mssg_parts[0] # fetching first element of the part 
                part_body = part_one['body'] # fetching body of the message
                part_data = part_body['data'] # fetching data from the body
                clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                clean_two = base64.b64decode (bytes(clean_one, 'ISO-8859-1')) # decoding from Base64 to UTF-8   
                soup = BeautifulSoup(clean_two , "lxml" )
                mssg_body = soup.body()
		
                temp_dict['Message_body'] = mssg_body

            except :
                pass

            # print (temp_dict)
            final_list.append(temp_dict) # This will create a dictonary item in the final list
	
	
            self.service.users().messages().modify(userId=user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
        return final_list

    def send(self,SENDER, RECIPIENT, SUBJECT, CONTENT):


        def create_message(sender, to, subject, message_text):
  
          message = MIMEText(message_text)
          message['to'] = to
          message['from'] = sender
          message['subject'] = subject
          encoded_message = urlsafe_b64encode(message.as_bytes())
          return {'raw': encoded_message.decode()}
          
        def send_message(user_id, message):
  
          try:
            message = (self.service.users().messages().send(userId=user_id, body=message)
               .execute())
            print('Send Message Id: %s' % message['id'])
            return message
          except:
            print('An error occurred')
        

        raw_msg = create_message(SENDER, RECIPIENT, SUBJECT, CONTENT)
        send_message("me", raw_msg)
        return raw_msg




# email = email()
# res = email.read()
# print(res)
# print ("Total messaged retrived: ", str(len(res)))