from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
import time
from datetime import datetime

def refresh_creds(creds):
    newcred = creds.refresh(Request())

def get_Credentials(val):
    creds = Credentials(
        token = val["token"],
        refresh_token=val["refresh_token"],
        token_uri=val["token_uri"],
        client_id=val["client_id"],
        client_secret=val["client_secret"],
        expiry=datetime.strptime(val["expiry"],"%Y-%m-%d %H:%M:%S"),
        scopes=val["scopes"],
    )
    return creds

if __name__ == "__main__":
    
    while True:
        with open ("token_res.json", "r") as f:
            data = json.load(f)
            for key,val in data.items():
                creds = get_Credentials(val)
                refresh_creds(creds)
                
                val["token"] = creds.token
                val["expiry"] = creds.expiry.strftime("%Y-%m-%d %H:%M:%S")
                val["refresh_token"] = creds.refresh_token

        with open("token_res.json", "w") as f:
            f.write(json.dumps(data,indent=4))
            print("refreshed tokens")
        time.sleep(3000)
