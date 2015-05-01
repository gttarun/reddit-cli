#!/usr/bin/python

# import sys

# arguments = sys.argv
# first_name  = sys.argv[1]
# second_name = sys.argv[2]

# print "Hello {0} {1} !!!!".format(first_name,second_name)


# from PIL import Image
# import urllib, cStringIO

# file = cStringIO.StringIO(urllib.urlopen("http://hairstyles.thehairstyler.com/hairstyle_views/front_view_images/464/original/10551_Jared-Padalecki_copy_2.jpg").read())
# img = Image.open(file)
# img.show()

import requests
from bs4 import BeautifulSoup

def pull_posts():
	headers = {'User-Agent': 'reddit-cli'}
	url = 'https://reddit.com/r/boxing'

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text)

	soup = soup.find(id='siteTable')
	parsed = soup(attrs={'class': 'thing'})
	parsed_more = [parsed(attrs={'class': 'title'}) for post in parsed]
