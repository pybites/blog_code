from collections import Counter
from itertools import dropwhile
import os
from pprint import pprint as pp
import re

from bs4 import BeautifulSoup as Soup
import requests

AMAZON = "amazon.com"
CACHED_HTML = "titans_books.html"
SHORT_SRC = "http://bit.ly/2gP0fv3"
TITLE = re.compile(r'.*{}/([^/]+).*'.format(AMAZON)).sub

def get_html():
    if os.path.isfile(CACHED_HTML):
        with open(CACHED_HTML) as f:
            html = f.read().lower()
    else:
        html = requests.get(SHORT_SRC).text
    return Soup(html)

def get_books():
    cnt = Counter()
    for a in get_html().find_all('a', href=True):
        href = a['href']
        if AMAZON in href:
            book = TITLE(r'\1', href)
            cnt[book] += 1
    return cnt


def get_multiple_mentions(books, keep=2):
    for key, count in dropwhile(lambda key_count: key_count[1] >= keep, books.most_common()):
        del books[key]
    return books


def print_results(books):
    for book, count in books.items():
        print("{:<3} {}".format(count, book))


if __name__ == "__main__":
    def test(cnt):
        assert(cnt["tao-te-ching-laozi"] == 3)
        assert(cnt["influence-psychology-persuasion-robert-cialdini"] == 2)
        assert(sum(cnt.values()) == 204)

    books = get_books()
    pp(books)
    test(books)
    multiple_mentions = get_multiple_mentions(books)
    print_results(multiple_mentions)
