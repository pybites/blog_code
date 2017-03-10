from collections import namedtuple
import datetime
import time

import requests
import requests_cache

requests_cache.install_cache()

Fork = namedtuple('Fork', 'url updated pushed')

USER = 'pybites'
REPO = 'challenges'
BASE_URL = 'https://api.github.com/repos/{}/{}'.format(USER, REPO)
FORK_URL = '{}/forks?page='.format(BASE_URL)


def get_num_pages():
    d = requests.get(BASE_URL).json()
    return int(d['network_count'] / 30) + 1


def get_utstamp(tstamp):
    dt = datetime.datetime.strptime(tstamp, "%Y-%m-%dT%H:%M:%SZ")
    return int(time.mktime(dt.timetuple()))


def last_change(f):
    updated = get_utstamp(f.updated)
    pushed = get_utstamp(f.pushed)
    return max(updated, pushed)


def get_forks(page_num):
    d = requests.get(FORK_URL + str(page_num)).json()
    for row in d:
        url = row['html_url']
        updated = row['updated_at']
        pushed = row['pushed_at']
        yield Fork(url, updated, pushed)


if __name__ == "__main__":
    num_forks_pages = get_num_pages()

    forks = {}
    for page_num in range(1, num_forks_pages + 1):
        for fork in get_forks(page_num):
            forks[fork.url] = fork

    fmt = '{:<60} | {:<20} | {:<20}'
    header = fmt.format(*Fork._fields)
    print(header)
    for fork in sorted(forks.values(), key=lambda x: last_change(x), reverse=True):
        entry = fmt.format(*fork)
        print(entry)
    print('Total forks: {}'.format(len(forks)))
