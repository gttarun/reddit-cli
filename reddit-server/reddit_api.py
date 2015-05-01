
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

package = 'Hello'
SECRET = 'fd340294sdkf9043ls'

CLIENT_ID = 'Ssu0fl-xIUrgYA'
CLIENT_SECRET = 'fUN46jr4FKuBr_GM1xEu8pDZcsw'
REDIRECT_URI = 'http://localhost:8080/authorize_callback'

class User(db.Model):
    hash_key = db.StringProperty()
    code = db.StringProperty()

class Code(messages.Message):
    hash_key = messages.StringField(1)
    url = messages.StringField(2)

@endpoints.api(name='redditapi', version='v0')
class RedditApi(remote.Service):

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage, hash_key=messages.StringField(1))

    @endpoints.method(ID_RESOURCE, Code, path='/{hash_key}', http_method='GET', name='')
 
    def get_code(self, request):
        if request.hash_key == "none":
            random_data = os.urandom(128)
            s = hashlib.md5(random_data).hexdigest()
            new_hash = hmac.new(SECRET, s, hashlib.sha256).hexdigest()
            
            r = praw.Reddit(user_agent='some_agent', disable_update_check=True)
            r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

            user = User()
            user.hash_key = new_hash
            code = "none"

            return Code(hash_key=new_hash, url=r.get_authorize_url('UniqueKey'))
        else:
            query = db.GqlQuery(
                "select * from User where hash_key=:1 limit 1", request.hash_key)
            user = query.get()

            return Code(hash_key=user.hash_key)

APPLICATION = endpoints.api_server([RedditApi])