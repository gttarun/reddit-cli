
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

jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

#OAuth settings
SECRET = os.environ['HASHSECRET']
CLIENT_ID = os.environ['REDDITID']
CLIENT_SECRET = os.environ['REDDITSECRET']
REDIRECT_URI = 'https://green-torus-802.appspot.com/authorize_callback'

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

        # Get username using code
        headers = {'user-agent': 'Reddit command line interface v0', 'Authorization': 'bearer ' + access_token}
        r = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        token_json = r.json()
        username = token_json['name']
        
        query = db.GqlQuery("select * from User where username=:1 limit 1", username)
        user = query.get()

        #If user exists
        if user:
            if user.hash_key: #If hash key exists
                user.code = access_token
                user.put()
        else:
            pass

    def post(self):
        pass

class MainPage(Handler):

    def get(self):
        pass

    def post(self):
        pass

app = webapp2.WSGIApplication([('/', MainPage), ('/authorize_callback', RedditAuthorize)], debug=True)
