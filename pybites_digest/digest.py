import os
import re
import sys
import time

import feedparser

DEFAULT_DAYS_BACK = 7
FEEDS = 'http://pybit.es/feeds'
RSS = 'all.rss.xml'
SECS_IN_DAY = 24 * 60* 60
ARTICLE_HTML = '''<article>
    <h2><a href="{}">{}</a></h2>
    {}
</article>'''
ARTICLE_TXT = '''{}
{}
{}
--
'''

def calc_utstamp_limit(days_back):
    now = int(time.time())
    return now - (days_back * SECS_IN_DAY)

def get_articles(utstamp_limit):
    xml = RSS if os.path.isfile(RSS) else os.path.join(FEEDS, RSS)
    feed = feedparser.parse(xml)
    for article in feed['entries']:
        utstamp = time_to_unix(article['published_parsed'])
        if utstamp < utstamp_limit:
            continue
        yield article

def time_to_unix(t):
    return int(time.mktime(t))

def strip_html(text):
    return re.sub('<[^<]+?>', '', text)

if __name__ == "__main__":
    days_back = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DAYS_BACK
    html = True if len(sys.argv) > 2 else False
    utstamp_limit = calc_utstamp_limit(days_back)
    for article in get_articles(utstamp_limit):
        if html:
            print(ARTICLE_HTML.format(article['link'], 
                  article['title'], article['summary']))
        else:
            print(ARTICLE_TXT.format(article['title'], 
                  article['link'], strip_html(article['summary'])))
