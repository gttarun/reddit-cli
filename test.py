

import requests


#r = requests.get('http://localhost:8080/_ah/api/user/tabchas')
# r = requests.get('https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/tabchas')
# print r.text

CLIENT_ID = 'Ssu0fl-xIUrgYA'
CLIENT_SECRET = 'fUN46jr4FKuBr_GM1xEu8pDZcsw'
#REDIRECT_URI = 'http://green-torus-802.appspot.com/authorize_callback'
REDIRECT_URI = 'http://localhost:8080/authorize_callback'

client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
post_data = {"grant_type": "authorization_code", "code": 'GUQJRqoYjJBxed1domJpIX7AGwc', "redirect_uri": REDIRECT_URI}
        
response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data)
token_json = response.json()
print token_json
#access_token = token_json["access_token"]
#print access_token