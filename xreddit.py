import requests
from bs4 import BeautifulSoup

def get_posts():

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

def main():
    posts = get_posts()

    for post in posts:
        print post, ' \n'

    return

main()
