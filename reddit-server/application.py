
import os
import webapp2
import jinja2
import urllib
import urllib2
import json
import hmac
import hashlib

import praw
import requests
import requests.auth

from google.appengine.ext import db

SECRET = 'fd340294sdkf9043ls'

# Riot API Key
# api_key = os.environ['RIOTAPIKEY']

jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

CLIENT_ID = 'Ssu0fl-xIUrgYA'
CLIENT_SECRET = 'fUN46jr4FKuBr_GM1xEu8pDZcsw'
#REDIRECT_URI = 'http://green-torus-802.appspot.com/authorize_callback'
REDIRECT_URI = 'http://localhost:8080/authorize_callback'

class User(db.Model):
    hash_key = db.StringProperty()
    username = db.StringProperty()
    code = db.StringProperty()

class Handler(webapp2.RequestHandler):

    def hash_str(self, s):
        return hmac.new(SECRET, s, hashlib.sha256).hexdigest()

    def make_secure_val(self, s):
        return "%s|%s" % (s, self.hash_str(s))

    def check_secure_val(self, h):
        if h == None:
            return None
        val = h.split('|')[0]
        if h == self.make_secure_val(val):
            return val
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class RedditAuthorize(Handler):

    def get(self):
        
        code = self.request.get('code')
        
        # Retrieve access token using code
        client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        post_data = {"grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI}
        
        response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data)
        token_json = response.json()
        access_token = token_json["access_token"]

        username = 'tabchas'
        query = db.GqlQuery("select * from User where username=:1 limit 1", username)
        user = query.get()
        user.code = access_token
        user.put()
        
        # Get username using code
        # headers = {'user-agent': 'reddit command line interface', 'Authorization': 'bearer ' + code}
        # r = requests.get('http://www.reddit.com/api/v1/me', headers=headers)
        # username = r.text

        
        # query = db.GqlQuery(
        #     "select * from User where username=:1 limit 1", username)
        # user = query.get()

        # #If user exists
        # if user:
        #     if user.hash_key: #If hash key exists
        #         user.code = access_token
        #         user.put()
        # else:
        #     pass

        #member = User()
        #member.hash_key = self.hash_str(code)
        #member.code = code
        #member.put()

    def post(self):
        pass

class MainPage(Handler):

    def get(self):
        
        r = praw.Reddit(user_agent='some_agent', disable_update_check=True)
        r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
        
        #Need to get permenant key somehow...
        self.redirect(r.get_authorize_url('UniqueKey', refreshable=True))

    def post(self):
        pass

app = webapp2.WSGIApplication([('/', MainPage), ('/authorize_callback', RedditAuthorize)], debug=True)
