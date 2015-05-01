
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

from google.appengine.ext import db

SECRET = 'fd340294sdkf9043ls'

# Riot API Key
# api_key = os.environ['RIOTAPIKEY']

jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

CLIENT_ID = 'Ssu0fl-xIUrgYA'
CLIENT_SECRET = 'fUN46jr4FKuBr_GM1xEu8pDZcsw'
REDIRECT_URI = 'http://localhost:8080/authorize_callback'

class User(db.Model):
    hash_key = db.StringProperty()
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

        member = User()
        member.hash_key = self.hash_str(code)
        member.code = code
        member.put()

    def post(self):
        pass

class MainPage(Handler):

    def get(self):
        
        r = praw.Reddit(user_agent='some_agent', disable_update_check=True)
        r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
        
        #Need to get permenant key somehow...
        self.redirect(r.get_authorize_url('UniqueKey'))

    def post(self):
        pass

app = webapp2.WSGIApplication([('/', MainPage), ('/authorize_callback', RedditAuthorize)], debug=True)
