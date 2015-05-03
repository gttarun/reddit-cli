
import requests, cmd, os, json, webbrowser
from bs4 import BeautifulSoup

def get_posts(subreddit='', previous=False, next=False, hot=''):

    # set user agent and url to request response from reddit
    headers = {'User-Agent': 'Reddit command line interface v0'}
    
    if (subreddit):
        if subreddit == '..':
            url = 'https://reddit.com' # back to main reddit page
        else:
            url = 'https://reddit.com/r/' + subreddit # subreddit page
    else:
        url = 'https://reddit.com'

    # change html response into bs4 object and parse data 
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html)
    parsed = soup.find(id='siteTable')

    # extract just the title of the post and its link
    pre_posts = [post.find('p', attrs={'class' : 'title'}) for post in parsed(attrs={'class': 'thing'})]
    posts = [[post.find('a').get('href'), post.get_text()] for post in pre_posts]

    # to get the unique post id and it to posts list
    post_id = [id_post.find('a').get('href') for id_post in parsed(attrs={'class': 'first'})]
    for i in range(len(post_id)):
        posts[i].append(post_id[i])

    return posts # a list of posts with title and links

def store_hash(hash_code):
    if hash_code:
        hash_file = open("hash.txt", "a")
        hash_file.write(hash_code)
        hash_file.close()
    return

class HackerCmd(cmd.Cmd):
    """Simple command processor example."""

    def do_login1(self, username):
        # if not os.path.isfile("hash.txt"): 
        #     resp = requests.get("https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/" + username)
        #     data = json.loads(resp.text)

        #     store_hash(data['hash_key'])
        #     webbrowser.open(data['url'])

        self.user = username
        self.old_count = 1
        self.posts = [] # empty list to contain posts of a <subreddit> if specified
        self.count = 1 # set count
        print "Welcome", self.user
    
    def do_feed1(self, subreddit=''):
        self.subreddit = subreddit # set subreddit for future navigation
        self.posts.extend(get_posts(subreddit))

        # navigating posts info.
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'

        if self.count == 1:
            print '\t', self.posts[0][1][:100], '..\n'
        for i in range(self.count, len(self.posts)):
            print i, '::\t', self.posts[i][1][:100], '..\n'

    def do_view(self, post):
        try:
            print self.posts[eval(post) - 1][0]
        except:
            print '\nERROR: Please specify "feed" to view a post, feed <none> or feed <subreddit>'

    def do_next(self, forward):
        next_page = self.posts[-1][2].split("/")
        next_key = [next_page[i + 1] for i in range(len(next_page)) if next_page[i] == 'comments']

        self.old_count = self.count
        self.count = len(self.posts)
        self.posts.extend(get_posts(self.subreddit + '/?count=' + str(len(self.posts) - 1) + '&after=t3_' + str(next_key[0])))
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'
        if self.count == 1:
            print '\t', self.posts[0][1][:100], '..\n'
        for i in range(self.count, len(self.posts)):
            print i, '::\t', self.posts[i][1][:100], '..\n'

    def do_prev(self, back):
        self.count, self.old_count = self.old_count, self.count
        print '\n', '/r/' + self.subreddit, 'subreddit'
        print '[to view post, "view #"] [main reddit page, "feed .."]\n'
        if self.count == 1:
            print '\t', self.posts[0][1][:100], '..\n'
        for i in range(self.count, self.old_count):
            print i, '::\t', self.posts[i][1][:100], '..\n'

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