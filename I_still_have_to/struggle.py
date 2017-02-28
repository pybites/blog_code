from pprint import pprint as pp
import sys
import time

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

NOW = int(time.time())
SEARCH = 'my name is years python'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


def get_tweets(search):
    for tweet in tweepy.Cursor(api.search,
                               q=search,
                               rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():
        if not tweet.retweeted and 'RT @' not in tweet.text:
            yield tweet


if __name__ == "__main__":
    if len(sys.argv) > 1:
        search = ' '.join(sys.argv[1:])
    else:
        search = SEARCH

    outfile = 'data_{}.txt'.format(NOW)
    with open(outfile, 'w') as f:
        for tweet in get_tweets(search):
            pp(tweet)
            f.write('{}\n'.format(tweet.text))
