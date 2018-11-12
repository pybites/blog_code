from collections import defaultdict
import re

import requests

GH_API_PULLS_ENDPOINT = 'https://api.github.com/repos/pybites/challenges/pulls'
PR_LINK = "https://github.com/pybites/challenges/pull/{id}"
CHALLENGE_LINK = "http://codechalleng.es/challenges/{id}"
EXTRACT_TEMPLATE = re.compile(r'.*learn\?\):\s+\[(.*?)\]Other.*')


def get_learning(template):
    """Helper to extract learning from PR template"""
    learning = ''.join(template.split('\r\n'))
    return EXTRACT_TEMPLATE.sub(r'\1', learning).strip()


def get_open_prs():
    """Parse GH API pulls JSON into a dict of keys = code challenge ids
       and values = lists of (pr_number, learning) tuples"""
    open_pulls = requests.get(GH_API_PULLS_ENDPOINT).json()
    prs = defaultdict(list)

    for pull in open_pulls:
        pr_number = pull['number']

        pcc = pull['head']['ref'].upper()
        learning = get_learning(pull['body'])
        if learning:
            prs[pcc].append((pr_number, learning))

    return prs


def print_review_markdown(prs):
    """Return markdown for review post, e.g.
       https://pybit.es/codechallenge57_review.html ->
       Read Code for Fun and Profit"""
    for pcc, prs in sorted(prs.items()):
        challenge_link = CHALLENGE_LINK.format(id=pcc.strip('PCC'))
        print(f'\n#### [{pcc}]({challenge_link})')

        for i, (pr_number, learning) in enumerate(prs):
            if i > 0:
                print('\n<!-- -->')
            pr_link = PR_LINK.format(id=pr_number)
            print(f'\n> {learning} - [PR]({pr_link})')


if __name__ == '__main__':
    prs = get_open_prs()
    print_review_markdown(prs)
