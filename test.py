

import requests


#r = requests.get('http://localhost:8080/_ah/api/user/tabchas')
r = requests.get('https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/tabchas')
print r.text