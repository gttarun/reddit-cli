
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

import hashlib
import os
import hmac

import praw
import requests

from google.appengine.ext import db

SECRET = os.environ['HASHSECRET']
CLIENT_ID = os.environ['REDDITID']
CLIENT_SECRET = os.environ['REDDITSECRET']
REDIRECT_URI = 'https://green-torus-802.appspot.com/authorize_callback'

'''
Add two columns
    Old hash and old code

Scenarios:

1st timer:
    Sends over username, returns URL + hash_key
    Clicks URL, redirected to Reddit

    On success:
        Server stores code as username:code
    On fail:
        Server does nothing

Lost hash.txt:
    Checks hash.txt file

    Sends over username, web server sees already exist
        Deletes, old hash, disables code
        returns URL + hash_key
        Clicks URL, redirected to Reddit

        On success:
            Server stores code as username:code
        On fail:
            Server does nothing

Using someone elses username:
    Text file exists:
        Sends ur hash, with someone elses username:
            returns error

    Text file doesnt exist:
        Sends over username, returns URL + hash_key

        Clicks URL, redirected to Reddit

        On success:
            Server stores code as username:code
        On fail:
            Server does nothing
'''

class User(db.Model):
    hash_key = db.StringProperty()
    username = db.StringProperty()
    code = db.StringProperty()

class Code(messages.Message):
    hash_key = messages.StringField(1)
    url = messages.StringField(2)
    code = messages.StringField(3)

@endpoints.api(name='redditapi', version='v0')
class RedditApi(remote.Service):

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage, hash_key=messages.StringField(1))

    @endpoints.method(ID_RESOURCE, Code, path='/hash/{hash_key}', http_method='GET', name='')
 
    def get_code(self, request):

        query = db.GqlQuery(
                "select * from User where hash_key=:1 limit 1", request.hash_key)
        user = query.get()

        if user:     
            return Code(code=user.code)

    ID_RESOURCE2 = endpoints.ResourceContainer(
        message_types.VoidMessage, username=messages.StringField(1))

    @endpoints.method(ID_RESOURCE2, Code, path='/user/{username}', http_method='GET', name='')
 
    def get_hash(self, request):

        query = db.GqlQuery(
                "select * from User where username=:1 limit 1", request.username)
        user = query.get()

        if not user:
            random_data = os.urandom(128)
            s = hashlib.md5(random_data).hexdigest()
            new_hash = hmac.new(SECRET, s, hashlib.sha256).hexdigest()
            
            r = praw.Reddit(user_agent='reddit command line interface', disable_update_check=True)
            r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

            user = User()
            user.username = request.username
            user.hash_key = new_hash
            user.code = "none"
            user.put()

            return Code(hash_key=new_hash, url=r.get_authorize_url('UniqueKey', scope=['identity'], refreshable=True))
        else:
            query = db.GqlQuery(
                "select * from User where username=:1 limit 1", request.username)
            user = query.get()

            return Code(hash_key=user.hash_key)

APPLICATION = endpoints.api_server([RedditApi])