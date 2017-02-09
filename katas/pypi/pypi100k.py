from datetime import datetime
import os
from pprint import pprint as pp
from time import mktime
import sys

import bs4
import feedparser
import requests

NUM_PACKS_TO_REACH = 100_000
NOW = datetime.utcnow()
PYPI = 'https://pypi.python.org/pypi'
PYPI_OUT = 'pypi.html'
RSS = 'https://pypi.python.org/pypi?%3Aaction=packages_rss'
RSS_OUT = 'feed.rss'
REFRESH = True


def get_feed(rss, fname):
    r = requests.get(rss)
    if r.status_code != 200:
        sys.exit('cannot get feed')
    with open(fname, 'w') as f:
        f.write(r.text)


def get_current_num_packages():
    if not os.path.isfile(PYPI_OUT) or REFRESH:
        get_feed(PYPI, PYPI_OUT)
    with open(PYPI_OUT) as f:
        soup = bs4.BeautifulSoup(f.read(), "lxml")
        div = soup.find('div', {"class":"section"})
        try:
            return int(div.find('strong').text)
        except:
            sys.exit('Cannot scrape number of package')


def main():
    if not os.path.isfile(RSS_OUT) or REFRESH:
        get_feed(RSS, RSS_OUT)

    num_packages = get_current_num_packages()

    with open(RSS_OUT) as f:
        html = f.read()
        items = feedparser.parse(html)
        dates = [datetime.fromtimestamp(mktime(item['published_parsed'])) for item in items['entries']]
        avg_addtime = (max(dates) - min(dates)) / len(dates)
        time_till_reach = avg_addtime * (NUM_PACKS_TO_REACH - num_packages) 
        print(NOW + time_till_reach)

if __name__ == "__main__":
    main()
