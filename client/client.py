# Importing Libraries

import json
import requests
import time
from conf import OauthId, ApiKey

url = "https://voice.octorgb.com"

# Getting Ngrok Info

try:
    r = requests.get("http://localhost:4040/api/tunnels")
    url = r.json()['tunnels'][0]['public_url']
    print(url)
except:
    print("Error getting Ngrok Info")

# Sending info to server

try:
    db = requests.post(url, data={'OauthId': OauthId, 'url': url, 'ApiKey': ApiKey})
    time.sleep(5)
    print(db.text)
except:
    print("Error sending info to the server")

