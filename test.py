

import requests


r = requests.get('http://localhost:8080/_ah/api/user/tabchas')
print r.text