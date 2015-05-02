import requests, cmd
from bs4 import BeautifulSoup

def get_posts(subreddit='', previous=False, next=False, hot=''):

    # set user agent and url to request response from reddit
    headers = {'User-Agent': 'reddit-cli'}
    url = 'https://reddit.com/r/boxing'

    # change html response into bs4 object and parse data 
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html)
    parsed = soup.find(id='siteTable')

    # extract just the title of the post and its link
    pre_posts = [post.find('p', attrs={'class' : 'title'}) for post in parsed(attrs={'class': 'thing'})]
    posts = [[post.find('a').get('href'), post.get_text()] for post in pre_posts]
    
    return posts # a list of posts with title and links

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""

    def do_login(self, line):
        print "Welcome gattarun"
    
    def do_feed(self, line):
        print '\n/r/boxing/ subreddit \n[to view post, "view #"] [next page, "next"] [previous page, "prev"] [main reddit page, "feed .."]\n'
        for i in range(len(posts)):
            print i + 1, '::\t', posts[i][1][:100], '..\n'

    def do_view(self, post):
        print posts[eval(post) - 1][0]

    def do_quit(self, line):
        return True

if __name__ == '__main__':
    posts = get_posts()
    HelloWorld.prompt = 'xreddit > '
    HelloWorld().cmdloop()
