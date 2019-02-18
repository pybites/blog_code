import argparse
from collections import namedtuple
import os

from selenium import webdriver
import requests
import tweepy

PACKT_FREE_LEARNING = "https://www.packtpub.com/packt/offers/free-learning"
HELP_TEXT = 'Packt free book (video) of the day'
UPDATE_MSG = """Packt Free Learning of the day:
{title}
by {author} (published: {pub_date})
{link}

Expires in {expires} ... grab it now!

{cover}
"""
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
SLACK_WEBHOOK_URL = ''

Book = namedtuple('Book', 'title author pub_date cover expires')


def _create_update(book):
    return UPDATE_MSG.format(title=book.title,
                             author=book.author,
                             pub_date=book.pub_date,
                             link=PACKT_FREE_LEARNING,
                             timer=book.expires,
                             cover=book.cover)


def get_packt_book():
    driver = webdriver.Chrome()
    driver.get(PACKT_FREE_LEARNING)

    find_class = driver.find_element_by_class_name
    title = find_class('product__title').text
    author = find_class('product__author').text
    pub_date = find_class('product__publication-date').text
    cover = find_class('product__img').get_attribute("src")

    timer = find_class('countdown__title').text
    hours = timer.split()[-1].split(':')[0]
    expires = f'in {hours} hours'

    driver.quit()

    book = Book(title, author, pub_date, cover, expires)
    update = _create_update(book)
    return update


def twitter_authenticate():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


def post_to_twitter(book_post):
    try:
        api = twitter_authenticate()
        api.update_status(book_post)
        print(f'Shared title on Twitter')
    except Exception as exc:
        print(f'Error posting to Twitter - exception: {exc}')


def post_to_slack(book_post):
    try:
        resp = requests.post(SLACK_WEBHOOK_URL,
                             json={'text': book_post})
        import pdb; pdb.set_trace()
        if resp.status_code == 201:
            print(f'Shared title on Slack')
        else:
            raise
    except Exception as exc:
        print(f'Error posting to Slack - exception: {exc}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument('-t', '--twitter', action='store_true',
                        help="Post title to Twitter")
    parser.add_argument('-s', '--slack', action='store_true',
                        help="Post title to Slack")
    args = parser.parse_args()

    book_update = get_packt_book()
    print(book_update)

    if args.slack:
        post_to_twitter(book_update)

    if args.twitter:
        post_to_slack(book_update)
