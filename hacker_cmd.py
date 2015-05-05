
import requests, cmd, os, json, webbrowser
from bs4 import BeautifulSoup
from PIL import Image
import requests
from StringIO import StringIO

# NEED TO BE DONE

# some pages have an extra post with no rank and others don't, sort accordingly
# check {attr['class': 'domain']} for the redirect site (reddit, facebook, youtube, etc)
# include number of upvotes
# also need to probably  include a way to upvote as user, api call?
# message system @user
# different tabs in each subreddit (hot, new, rising, controversial, etc.)
# clean up

def get_posts(subreddit='', sort=''):

    # set user agent and url to request response from reddit
    headers = {'User-Agent': 'Reddit command line interface v0'}
    
    # load page response according t subreddit & sort category (hot, new, rising, etc)
    if subreddit == '..' or subreddit == 'home':
        url = 'https://reddit.com'
    elif subreddit:
        url = 'https://reddit.com/r/' + subreddit
    else:
        url = 'https://reddit.com'

    url = url + '/' + sort

    # change html response into bs4 object and parse data
    try: 
        response = requests.get(url, headers=headers)
    except:
        print "ERROR: invalid request, and or could not recieve response from %s" %url
        return {} # bad response

    html = response.text
    soup = BeautifulSoup(html)
    parsed = soup.find(id='siteTable')
    
    # get all atributes of a post
    rank = [post.get_text() for post in parsed(attrs={'class': 'rank'})]
    title = [post.get_text() for post in parsed(attrs={'class': 'title may-blank '})]
    domain = [post.get_text() for post in parsed(attrs={'class': 'domain'})]
    link = [post.get('href') for post in parsed(attrs={'class': 'title may-blank '})]
    flair = [post.get_text() for post in parsed(attrs={'class': 'linkflairlabel'})]
    post_id = [post.get('data-fullname') for post in parsed(attrs={'class' : 'thing'})]
    score = [post.get_text() for post in parsed(attrs={'class': 'score unvoted'})]
    comments = [post.get_text() for post in parsed(attrs={'class': 'first'})]
    extra = [id_post.find('a').get('href') for id_post in parsed(attrs={'class': 'first'})]

    posts = {}

    # create a dictionary containing posts and info. for each of them
    for i in range(len(rank)):
        if rank[i] == '':
            rank[i] = '0'
        posts[eval(rank[i])] = {'rank': eval(rank[i]), 'title':title[i], 'domain':domain[i], 
                            'link':link[i], 'post_id':post_id[i], 'score':score[i],
                            'comments':comments[i]}

    return posts # a list of posts with title and links

def get_hash(username):
    r = requests.get('https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/' + username)
    jsonOut = json.loads(r.text)
    return jsonOut['hash_key']

def store_hash(hash_code):
    if hash_code:
        hash_file = open("hash.txt", "w")
        hash_file.write(hash_code)
        hash_file.close()
    return

class HackerCmd(cmd.Cmd):
    """Simple command processor example."""

    # just some categoies to search for
    categories = ['boxing', 'movies', 'music', 'cooking', 'pics', 'leagueoflegends', 
                 'basketball', 'python', 'news', 'funny', 'jokes', 'art', 'fitness']

    # set username and initialize class variables
    def do_login(self, username):
        self.user = username
        self.page = 1
        self.posts = {}
        self.subreddit = ''
        self.sort = ''

        # hash_key = get_hash(self.user)
        # store_hash(hash_key)

        print "Welcome HACKER!"

    # can change subreddit in a more familiar way :)
    def do_cd(self, subreddit=''):
        self.subreddit = subreddit.split(' ')[0]
        try:
            self.sort = subreddit.split(' ')[1]
        except:
            pass
        if subreddit != self.subreddit:
            self.page = 1
            self.start = 0
            self.limit = 8
            self.posts = {}
    
    # show specified <subreddit> feed
    def do_feed(self, not_used):
        self.start = 0
        self.limit = 8
        self.posts.update(get_posts(self.subreddit, self.sort)) # populate dictionary

        # navigating posts info.
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'

        if not self.posts:
            print "oops, there doesn't seem to be anything here\n"
            return

        for rank in range(self.start, self.limit):
            try:
                print self.posts[rank]['rank'],'|\t',  self.posts[rank]['score'], '::\t', self.posts[rank]['title'][:75] + '..', self.posts[rank]['domain']
                print "\t\t", self.posts[rank]['comments'], '\n'
            except:
                pass

    def do_next(self, not_used):
        self.start = self.limit
        self.limit += 8
        if self.limit > len(self.posts):
            self.start = len(self.posts)
            self.subreddit = self.subreddit + '/?count=' + str(len(self.posts) - 1) + '&after=' + self.posts[len(self.posts) - 1]['post_id']
            self.posts.update(get_posts(self.subreddit)) # populate dictionary
            self.page += 1
            self.limit += 8

         # navigating posts info.
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'

        for rank in range(self.start, self.limit):
            try:
                print self.posts[rank]['rank'],'|\t',  self.posts[rank]['score'], '::\t', self.posts[rank]['title'][:75] + '..', self.posts[rank]['domain']
                print "\t\t", self.posts[rank]['comments'], '\n'
            except:
                pass

    def do_prev(self, not_used):
        self.start -= 8
        self.limit -= 8
        if self.start < 0:
            self.start = 0
        if self.limit <= 0:
            self.limit = 8

         # navigating posts info.
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'

        for rank in range(self.start, self.limit):
            try:
                print self.posts[rank]['rank'],'|\t',  self.posts[rank]['score'], '::\t', self.posts[rank]['title'][:75] + '..', self.posts[rank]['domain']
                print "\t\t", self.posts[rank]['comments'], '\n'
            except:
                pass

    def do_view(self, rank):
        rank = eval(rank)
        if (self.posts[rank]['link'][:3] == '/r/'):
            webbrowser.open('https://www.reddit.com' + self.posts[rank]['link'])
            return
        else:
            if ('imgur' in self.posts[rank]['link']):
                if ('i.imgur' in self.posts[rank]['domain']):
                    response = requests.get(self.posts[rank]['link'])
                else:
                    response = requests.get('i.' + self.posts[rank]['link'])
                img = Image.open(StringIO(response.content))
                img.show()
                return
            webbrowser.open(self.posts[rank]['link'])
            return

        print '\nERROR: Please specify "feed" to view a post, feed <none> or feed <subreddit>'

    def complete_feed(self, text, line, begidx, endidx):
        if not text:
            completions = self.categories[:]
        else:
            completions = [ f
                            for f in self.categories
                            if f.startswith(text)
                            ]
        return completions

    # for TESTING
    def do_show(self, rank):
        rank = eval(rank)
        print self.posts[rank]['link']
        print self.posts[rank]['domain']

    def do_help(self, t):
        print "\nxreddit help\n------------"
        print "login <username>"
        print "feed <none> <sort> or feed <subreddit> <sort> or feed <..> (return back to main reddit)"
        print "view <rank>"
        print "next (load next page of feed)"
        print "prev (load previous page of feed)"
        print "quit"
        print "\nfor more help, type help(<key>)\n"

    def do_quit(self, line):
        return True
