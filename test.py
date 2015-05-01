

import requests

#r = requests.get('http://localhost:8080/_ah/api/helloworld/v1/hellogreeting/')
headers = {
    'User-Agent': 'I am building a command line interface for reddit :)'
}

r = requests.get('http://www.reddit.com/r/boxing/hot')

print r.text