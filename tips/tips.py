from collections import namedtuple
from random import choice
from time import sleep
import urllib.parse

from bs4 import BeautifulSoup
import requests
from selenium import webdriver

TIPS_PAGE = 'https://codechalleng.es/tips'
PYBITES_HAS_TWEETED = 'pybites/status'
CARBON = 'https://carbon.now.sh/?l=python&code={code}'
TWEET_BTN_CLASS = 'jsx-2739697134'
TWEET = '''{tip} {src}

🐍 Check out more @pybites tips at https://codechalleng.es/tips 💡

(Image built with #Carbon, by @dawn_labs)

{img}
'''

Tip = namedtuple('Tip', 'tip code src')


def retrieve_tips():
    """Grab and parse all tips from https://codechalleng.es/tips
       returning a list of Tip namedtuples
    """
    html = requests.get(TIPS_PAGE)

    soup = BeautifulSoup(html.text, 'html.parser')
    trs = soup.findAll("tr")

    tips = []

    for tr in trs:
        tds = tr.find_all("td")
        td = tds[1]

        links = td.findAll("a", class_="left")
        share_link = links[0].attrs.get('href')

        pre = td.find("pre")
        code = pre and pre.text or ''

        # skip if tweeted or not code in tip
        if PYBITES_HAS_TWEETED in share_link or not code:
            continue

        tip = td.find("blockquote").text
        src = len(links) > 1 and links[1].attrs.get('href') or ''

        tips.append(Tip(tip, code, src))

    return tips


def get_carbon_image(tip):
    """Visit carbon.now.sh with the code, click the Tweet button
       and grab and return the Twitter picture url
    """
    code = urllib.parse.quote_plus(tip.code)
    url = CARBON.format(code=code)

    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element_by_class_name(TWEET_BTN_CLASS).click()
    sleep(3)  # this might take a bit

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    status = driver.find_element_by_id('status')
    img = status.text.split(' ')[-1]

    driver.quit()
    return img


if __name__ == '__main__':
    tips = retrieve_tips()
    tip = choice(tips)

    src = tip.src and f' - see {tip.src}' or ''
    img = get_carbon_image(tip)

    tweet = TWEET.format(tip=tip.tip, src=src, img=img)
    # TODO: auto-post to twitter + POST link back to Tips API
    # but a bit of manual checking of the generated tweet is ok for now
    print(tweet)
