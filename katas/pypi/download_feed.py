import urllib2
import time

FEED = 'https://pypi.python.org/pypi?%3Aaction=packages_rss'
NOW = str(int(time.time()))
FILE_NAME = 'feed_{}.rss'.format(NOW)

response = urllib2.urlopen(FEED)
html = response.read()
with open(FILE_NAME, 'w') as f:
    f.write(html)
