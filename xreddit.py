import requests, cmd, os
from bs4 import BeautifulSoup

set_posts = []

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

def store_hash(hash_code=''):
    if hash_code:
        w_directory = os.getcwd()
        hash_file = open(w_directory + "hash.txt", "a")
        hash_file.write(hash_code)
        hash_file.close()
    return

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""

    user = ''

    def do_login(self, username):
        if not username:
            print "Please login with your <username>"
            return

        # import os.path
        # os.path.isfile(fname) 

        resp = requests.get("https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/" + username)
        data = json.loads(resp.text)
            
        global user
        user = username
        print "Welcome", username
    
    def do_feed(self, subreddit=''):
        if user:
            posts = get_posts(subreddit)
            global set_posts
            set_posts = posts
            print '\n', '/r/' + subreddit, 'subreddit'
            print '[to view post, "view #"] [main reddit page, "feed .."]\n'
            for i in range(len(posts)):
                print i + 1, '::\t', posts[i][1][:100], '..\n'
        else:
            print "Please login with your <username>"
            return

    def do_view(self, post):
        try:
            print set_posts[eval(post) - 1][0]
        except:
            print '\nERROR: Please specify "feed" to view a post, feed <none> or feed <subreddit>'

    def do_next(self):
        pass

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

# https://green-torus-802.appspot.com/_ah/api/redditapi/v0/user/ GAE
