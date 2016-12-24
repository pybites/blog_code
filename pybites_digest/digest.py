from datetime import datetime
import os
import re
import sys
import time

import feedparser

DEFAULT_DAYS_BACK = 7
FEEDS = 'http://pybit.es/feeds'
RSS = 'all.rss.xml'
SECS_IN_DAY = 24 * 60* 60
TITLE = '<h1>PyBites weekly digest</h1>'
ARTICLE_HTML = '''<article>
    <h2><a href="{}">{}</a></h2>
    {}
</article>'''

def calc_utstamp_limit(days_back):
    now = int(time.time())
    return now - (days_back * SECS_IN_DAY)

def get_articles(utstamp_limit):
    xml = RSS if os.path.isfile(RSS) else os.path.join(FEEDS, RSS)
    feed = feedparser.parse(xml)
    for e in feed['entries']:
        utstamp = time_to_unix(e['published_parsed'])
        if utstamp < utstamp_limit:
            continue
        yield ARTICLE_HTML.format(
            e['link'], e['title'], e['summary']
        )

def time_to_unix(t):
    return int(time.mktime(t))

if __name__ == "__main__":
    days_back = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DAYS_BACK
    utstamp_limit = calc_utstamp_limit(days_back)
    print(TITLE)
    for article in get_articles(utstamp_limit):
        print(article)
