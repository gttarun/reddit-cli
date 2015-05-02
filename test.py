

import requests
#import urllib2

# #r = requests.get('http://localhost:8080/_ah/api/user/tabchas')
# # r = requests.get('https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/tabchas')
# # print r.text

CLIENT_ID = 'rqtEo4z9O6Wsog'
CLIENT_SECRET = 'azsGqm3Zm8BBEe6DMfD83Cze9jM'
#REDIRECT_URI = 'http://green-torus-802.appspot.com/authorize_callback'
REDIRECT_URI = 'https://green-torus-802.appspot.com/authorize_callback'

# client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
# headers = {
#     'User-Agent': 'reddit command line interface v0'
# }

# post_data = {"grant_type": "authorization_code", "code": 'qcS7mEhEz6DjgWs3HaPtyUD8zSY', "redirect_uri": REDIRECT_URI}
        
# response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, headers=headers, data=post_data)
# token_json = response.json()
# access_token = token_json["access_token"]
# print access_token

headers = {'user-agent': 'reddit command line interface', 'Authorization': 'bearer ' + '22711848-uibvSlB3lzyijzwR_VsYnaqb_vM'}
r = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
token_json = r.json()
print token_json
