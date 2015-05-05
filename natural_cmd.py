
import requests, cmd, os, json, webbrowser
from bs4 import BeautifulSoup

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
        url = 'http://reddit.com'

    url = url + '/' + sort

    # change html response into bs4 object and parse data 
    response = requests.get(url, headers=headers)
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
                            'comments':comments[i],'extra':extra[i]}

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

class RedditCmd(cmd.Cmd):
    """Simple command processor example."""

    # set username and initialize class variables
    def do_login(self, username):
        self.user = username
        self.page = 1
        self.posts = {}

        hash_key = get_hash(self.user)
        store_hash(hash_key)

        print "Welcome", self.user
    
    # show specified <subreddit> feed
    def do_feed(self, subreddit=''):
        self.subreddit = subreddit # set subreddit for future navigation
        self.posts.update(get_posts(subreddit)) # populate dictionary

        # navigating posts info.
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'

        for rank in range(len(self.posts)):
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
            webbrowser.open(self.posts[rank]['link'])
            return

        print '\nERROR: Please specify "feed" to view a post, feed <none> or feed <subreddit>'

    # for TESTING
    def do_show(self, rank):
        rank = eval(rank)
        print self.posts[rank]['link']
        print self.posts[rank]['domain']

    def do_help(self, t):
        print "\nxreddit help\n------------"
        print "login <username>"
        print "feed <none> or feed <subreddit> or feed <..> (return back to main reddit)"
        print "view <post::number>"
        print "next (load next page of feed)"
        print "prev (load previous page of feed)"
        print "quit"
        print "\nfor more help, type help(<key>)\n"

    def do_quit(self, line):
        return True
