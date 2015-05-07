
import requests, cmd, os, json, webbrowser
from bs4 import BeautifulSoup
from PIL import Image
import requests
from StringIO import StringIO

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
    html = html[html.find('<div id="siteTable" class="sitetable linklisting">'):]
    soup = BeautifulSoup(html)
    parsed = soup.findAll("div", attrs={ "class" : "thing" })
    
    # get all atributes of a post
    rank = [[rank.get_text() for rank in post(attrs={'class': 'rank'})] for post in parsed]
    title = [[title.get_text() for title in post(attrs={'class': 'title may-blank '})] for post in parsed]
    domain = [[domain.get_text() for domain in post(attrs={'class': 'domain'})] for post in parsed]
    link = [[link.get('href') for link in post(attrs={'class': 'title may-blank '})] for post in parsed]
    flair = [[tag.get_text() for tag in post(attrs={'class': 'linkflairlabel'})] for post in parsed]
    post_id = [post.get('data-fullname') for post in parsed]
    score = [[score.get_text() for score in post(attrs={'class': 'score unvoted'})] for post in parsed]
    comments = [[comment.get_text() for comment in post(attrs={'class': 'first'})] for post in parsed]

    # remove lists of list, create 1d list for all post attributes
    rank = [rank[i][0] for i in range(len(rank))]
    title = [title[i][0] for i in range(len(title))]
    domain = [domain[i][0] for i in range(len(domain))]
    link = [link[i][0] for i in range(len(link))]
    post_id = [post_id[i][0] for i in range(len(post_id))]
    score = [score[i][0] for i in range(len(score))]
    comments = [comments[i][0] for i in range(len(comments))]

    posts = {}

    # create a dictionary containing posts and info. for each of them
    for i in range(len(rank)):
        if rank[i] == '':
            rank[i] = '0'
        posts[eval(rank[i])] = {'rank': eval(rank[i]), 'title':title[i], 'domain':domain[i], 
                            'link':link[i], 'post_id':post_id[i], 'score':score[i],
                            'comments':comments[i]}
        try:
            posts[eval(rank[i])]['flair'] = flair[i][0]
        except:
            posts[eval(rank[i])]['flair'] = ''

    return posts # a list of posts with title and links

def get_token():
    with open('hash.txt', 'r') as hash_file:
        hash_key = hash_file.readline()

    r = requests.get('https://green-torus-802.appspot.com/_ah/api/redditapi/v0/hash/' + hash_key)
    jsonOut = json.loads(r.text)
    return jsonOut['access_token']

def get_hash(username):
    r = requests.get('https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/' + username)
    jsonOut = json.loads(r.text)
    return jsonOut

def store_hash(hash_code):
    if hash_code:
        hash_file = open("hash.txt", "w")
        hash_file.write(hash_code)
        hash_file.close()
    return

class RedditCmd(cmd.Cmd):
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
        
        # if os.path.isfile("hash.txt"):
        #     self.token = get_token()
        #     print self.token
        # else:
        #     jsonData = get_hash(username)
        #     authorize_url = jsonData['url']
        #     hash_key = jsonData['hash_key']

        #     webbrowser.open(authorize_url)

        #     store_hash(hash_key)

        print "Welcome", self.user
    
    # show specified <subreddit> feed
    def do_feed(self, subreddit=''):
        self.start = 1
        self.limit = 6

        # if user changes subreddit, remove previous history and clear everything
        if subreddit != self.subreddit:
            self.posts = {}
            self.page = 1

        self.subreddit = subreddit.split(' ')[0]
        try:
            self.sort = subreddit.split(' ')[1]
        except:
            pass
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
                print "\t\t", self.posts[rank]['comments'], '\t\t\t', self.posts[rank]['flair'], '\n'
            except:
                pass

    def do_next(self, not_used):
        self.start = self.limit
        self.limit += 5
        if (self.limit % (self.page * 25)) == 6:
            self.subreddit = self.subreddit + '/?count=' + str(len(self.posts) - 1) + '&after=' + self.posts[len(self.posts) - 1]['post_id']
            self.posts.update(get_posts(self.subreddit)) # populate dictionary
            self.page += 1

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
        self.start -= 5
        self.limit -= 5
        if self.start < 0:
            self.start = 0
        if self.limit <= 0:
            self.limit = 5

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
            webbrowser.open('https://www.reddit.com' + self.posts[rank]['link'], new=2, autoraise=True) # why is this NOT working.. ?
            return
        else:
            if ('imgur' in self.posts[rank]['link']):
                if ('i.imgur' in self.posts[rank]['domain']):
                    response = requests.get(self.posts[rank]['link'])
                else:
                    response = requests.get('http://i.' + self.posts[rank]['link'][7:] + ".jpg")
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

    def do_switch(self, not_used):
        if self.subreddit:
            url = "https://www.reddit.com/r/" + self.subreddit
        else:
            url = "https://www.reddit.com/"
        webbrowser.open(url)

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
