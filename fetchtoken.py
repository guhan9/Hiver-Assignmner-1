from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime

import os

SCOPES = ["https://mail.google.com/", 
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/pubsub", 
            "https://www.googleapis.com/auth/gmail.readonly", 
            "https://www.googleapis.com/auth/gmail.labels", 
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/gmail.insert", 
            "https://www.googleapis.com/auth/gmail.compose"
        ]
data = {}
if os.path.exists("token_res.json"):
    with open("token_res.json",'r') as f:
        data = json.load(f)


flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail','v1',credentials=creds)
gmail_info = service.users().getProfile(userId='me').execute()

data[gmail_info["emailAddress"]] = { "token": creds.token, 
                                    "refresh_token": creds.refresh_token, 
                                    "expiry": creds.expiry.strftime("%Y-%m-%d %H:%M:%S"), 
                                    "token_uri": creds.token_uri, "client_id": creds.client_id, 
                                    "client_secret": creds.client_secret,
                                    "scopes":SCOPES
                                    }

with open("token_res.json",'w') as f:
    f.write(json.dumps(data,indent=4))
