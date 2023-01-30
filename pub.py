import json
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from refresh_creds import get_Credentials
# Email addresses of the accounts to watch

#Pub/Sub topic to send notifications to
topic_name = "projects/assignment-375119/topics/Assignment"

with open("token_res.json") as f:
    credentials_data = json.load(f)

for key,val in credentials_data.items():
    try:
        # Build the Gmail API client
        creds = get_Credentials(val)

        service = build('gmail', 'v1', credentials=creds)    
        # Create the watch request body
        request = {
            "topicName": topic_name,
            "labelIds": ["INBOX"],
        }
        # Create the watch resource
        watch_response = service.users().watch(userId='me', body=request).execute()
        credentials_data[key]['historyId'] = watch_response['historyId']

        print(f"Watch resource created for {key} with data: {watch_response}")
    
    except HttpError as error:
        print(f"An error occurred: {error}")

with open("token_res.json",'w') as f:
    json.dump(credentials_data,indent=4,fp=f)

while True:
    time.sleep(86400)