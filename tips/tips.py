from collections import namedtuple
from random import choice
import sys
from time import sleep
import urllib.parse

import requests
from selenium import webdriver

TIPS_PAGE = 'https://codechalleng.es/api/admin_tips'
PYBITES_HAS_TWEETED = 'pybites/status'
CARBON = 'https://carbon.now.sh/?l=python&code={code}'
TWEET = '''{tip} {src}

🐍 Check out / submit more @pybites tips at https://codechalleng.es/tips 💡

(image built with @carbon_app)

{img}
'''

Tip = namedtuple('Tip', 'tip code link')


def retrieve_tips():
    """Grab and parse all tips from https://codechalleng.es/tips
       returning a dict of keys: tip IDs and values: Tip namedtuples
    """
    resp = requests.get(TIPS_PAGE)
    resp.raise_for_status()
    tips = {}

    for entry in resp.json():
        # skip tips that were already shared
        code = entry['code']
        if entry['share_link'] is not None or not code:
            continue

        idx = entry['id']
        tip = entry['tip']
        link = entry['link']

        tips[idx] = Tip(tip=tip, code=code, link=link)

    return tips


def get_carbon_image(tip):
    """Visit carbon.now.sh with the code, click the Tweet button
       and grab and return the Twitter picture url
    """
    code = urllib.parse.quote_plus(tip.code)
    url = CARBON.format(code=code)

    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element_by_xpath("//button[contains(text(),'Tweet')]").click()
    sleep(10)  # this might take a bit

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    status = driver.find_element_by_id('status')
    img = status.text.split(' ')[-1]

    driver.quit()
    return img


if __name__ == '__main__':
    tips = retrieve_tips()
    if len(sys.argv) == 2:
        tip_id = int(sys.argv[1])
    else:
        tip_id = choice(list(tips.keys()))

    tip = tips.get(tip_id)
    if tip is None:
        print(f'Could not retrieve tip ID {tip_id}')
        sys.exit(1)

    src = f' - see {tip.link}' if tip.link else ''
    img = get_carbon_image(tip)

    tweet = TWEET.format(tip=tip.tip, src=src, img=img)
    # TODO: auto-post to twitter + POST link back to Tips API
    # but a bit of manual checking of the generated tweet is ok for now
    print(tweet)
