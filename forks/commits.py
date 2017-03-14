from collections import namedtuple
import datetime
import time

import requests
import requests_cache

USER = 'pybites'
REPO = 'challenges'
BASE_URL = 'https://api.github.com/repos/{}/{}'.format(USER, REPO)
FORK_URL = '{}/forks?page='.format(BASE_URL)
HOUR_IN_SECONDS = 60 * 60

requests_cache.install_cache('cache', backend='sqlite', expire_after=HOUR_IN_SECONDS)

Fork = namedtuple('Fork', 'url updated pushed')

def get_utstamp(tstamp):
    dt = datetime.datetime.strptime(tstamp, "%Y-%m-%dT%H:%M:%SZ")
    return int(time.mktime(dt.timetuple()))


def last_change(f):
    updated = get_utstamp(f.updated)
    pushed = get_utstamp(f.pushed)
    return max(updated, pushed)


def get_forks():
    page_num = 0
    while True:
        page_num += 1
        url = FORK_URL + str(page_num)
        response = requests.get(url)
        # print('getting data for url {}'.format(url))
        d = response.json()
        if not d:
            return
        for row in d:
            url = row['html_url']
            updated = row['updated_at']
            pushed = row['pushed_at']
            yield Fork(url, updated, pushed)


if __name__ == "__main__":
    forks = {}
    for fork in get_forks():
        forks[fork.url] = fork

    fmt = '{:<60} | {:<20} | {:<20}'
    header = fmt.format(*Fork._fields)
    print(header)
    for fork in sorted(forks.values(), key=lambda x: last_change(x), reverse=True):
        entry = fmt.format(*fork)
        print(entry)
    print('Total forks: {}'.format(len(forks)))
