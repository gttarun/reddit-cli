import requests, cmd, os, json, webbrowser
from bs4 import BeautifulSoup

def get_posts(subreddit='', previous=False, next=False, hot=''):

    # set user agent and url to request response from reddit
    headers = {'User-Agent': 'reddit-cli'}
    
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

    return posts # a list of posts with title and links

def store_hash(hash_code):
    if hash_code:
        hash_file = open("hash.txt", "a")
        hash_file.write(hash_code)
        hash_file.close()
    return

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""

    def do_login(self, username):
        # if not os.path.isfile("hash.txt"): 
        #     resp = requests.get("https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/" + username)
        #     data = json.loads(resp.text)

        #     store_hash(data['hash_key'])
        #     webbrowser.open(data['url'])

        self.posts = [] # empty list to contain posts of a <subreddit> if specified
        self.count = 1 # set count
        print "Welcome", username
    
    def do_feed(self, subreddit=''):

        self.posts.extend(get_posts(subreddit))
        self.subreddit = subreddit
        print '\n', '/r/' + subreddit, 'subreddit'
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

    def do_next(self, use):
        next_page = self.posts[-1][0].split("/")
        next_key = [next_page[i + 1] for i in range(len(next_page)) if next_page[i] == 'comments']
        print next_page, next_key

        self.count = len(self.posts)
        #do_feed('/r/' + self.subreddit + '/?count=' + str(len(self.post) - 1) + '&after=t3_' + str(next_key))

    def do_prev(self):
        pass

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

if __name__ == '__main__':
    HelloWorld.prompt = 'xreddit > '
    HelloWorld().cmdloop()


