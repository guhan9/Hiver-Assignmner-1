import json
import time
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import pubsub_v1
from refresh_creds import get_Credentials
from email.mime.text import MIMEText
import email

TARGET_label = "Training Exercise"
project_id = "assignment-375119"
topic_id = "Assignment"
subscription_id = "Assignment-sub"

# Load credentials from token_res.json
with open("token_res.json") as f:
    credentials_data = json.load(f)
    EMAIL_LIST = credentials_data.keys()

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    mes = json.loads(message.data)
    email = mes['emailAddress']
    hist_id = mes['historyId']
    creds = get_Credentials(credentials_data[email])
    service = build('gmail', 'v1', credentials=creds)

    hist_list = service.users().history().list(
        userId='me',
        startHistoryId=credentials_data[email]['historyId'], 
        historyTypes="messageAdded").execute()

    credentials_data[email]['historyId'] = hist_id
    if len(hist_list) >= 2:
        message_ids = get_message_ids(hist_list) # obtain list of message id of new or sent emails
        # print(email,json.dumps(hist_list, indent=4),message_ids) 
        process_messages(service, message_ids)
    message.ack()

    with open("token_res.json", "w") as f:
        json.dump(credentials_data, f, indent=4)  # store updated history id

def get_message_ids(dic):
    message_ids = [] # store message id's in list
    for i in dic["history"]:
        for j in i["messagesAdded"]:
            if j["message"]['id'] not in message_ids and "DRAFT" not in j["message"]['labelIds'] :
                message_ids.append(j["message"]["id"])
    return message_ids

def process_messages(service, histories):
    for mesg_id in histories:
        raw_message = get_message(service, mesg_id, format = "raw") 

        msg_str = base64.urlsafe_b64decode(raw_message['raw']).decode()
        headers = email.message_from_string(msg_str)        

        #check subject of email 
        if raw_message and (headers['Subject'] == "Training Exercise" or headers['Subject'] == "Re: Training Exercise"):
            share_mail(headers,raw_message)

def get_message(service ,message_id,format = "full"):
    try:
        message = service.users().messages().get(userId='me', id=message_id,format = format).execute()
        return message
    except HttpError :
        return False

def share_mail(headers,raw_message):
    global_id = headers['Message-ID']
    for email in EMAIL_LIST:
        # create gmail service for perticular gmail account using OAuth token store in json file
        creds = get_Credentials(credentials_data[email])
        service = build('gmail', 'v1', credentials=creds)

        message_id = has_message(service, global_id) 
        if message_id.get('resultSizeEstimate',0) > 0:
            user_message = get_message(service, message_id['messages'][0]['id'])
            add_label(service, user_message)      
        else:
            insert_message(service,raw_message,headers)

def has_message(service, global_id):
    try:
        query = "rfc822msgid:"+global_id
        message = service.users().messages().list(userId='me',q = query).execute()
        return message
    except HttpError as error:
        print (f"An error occurred: {error}")
        return False

def insert_message(service,raw_message,headers):
    #inserts the mail and adds custom lable to the mail
    # If email is a reply
    if headers['in-reply-to']:
        # obtain threadId 
        Parent_msgid= headers['in-reply-to']
        mes_list = has_message(service, Parent_msgid) 
        if mes_list.get('resultSizeEstimate',0) > 0:
            thread_id = mes_list['messages'][0]['threadId']
            #insert into thread
            response = service.users().messages().insert(userId='me', body={'raw':raw_message['raw'],'labelIds':raw_message['labelIds'],'threadId':thread_id}).execute()
    else:
        #insert as new email thread
        response = service.users().messages().insert(userId='me', body={'raw':raw_message['raw'],'labelIds':raw_message['labelIds']}).execute()
    add_label(service, response)

def add_label(service, message):
    labels_list = get_labels(service) #list of lable id's for a email account

    if TARGET_label in labels_list.keys():
        label_id = labels_list[TARGET_label]
    else:
        label_id = create_label(service)
    
    # adds label to email
    if label_id not in message.get('labelIds',[]):
        request = {"addLabelIds": [label_id]}
        service.users().messages().modify(userId='me',id = message['id'],body = request).execute()
        return 

def get_labels(service):
    result = service.users().labels().list(userId='me').execute()
    return {label['name']: label['id'] for label in result['labels']}

def create_label(service):
    request = {
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
        "name": TARGET_label
    }
    response = service.users().labels().create(userId='me', body=request).execute()
    return response['id']

if __name__ == "__main__":

    #create a pub/sub subscriber to a topic
    creds = get_Credentials(credentials_data['gspam3218@gmail.com'])
    subscriber = pubsub_v1.SubscriberClient(credentials=creds)
    subscription_path = subscriber.subscription_path(
        project_id, subscription_id)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # keep program running   
    while True:
        time.sleep(0)