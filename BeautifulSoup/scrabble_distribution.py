#!python3
# scrape site with BeautifulSoup to get srabble distribution

from collections import namedtuple
import os
from string import ascii_uppercase

from bs4 import BeautifulSoup as Soup
import requests

URL = 'http://scrabblewizard.com/scrabble-tile-distribution/'
HTML = 'scrabble.html'
LETTERS = list(ascii_uppercase)  # exclude 2x blanks (scrabble wildcards)
LETTER_REPR = 'Letter: {} - amount: {} / value: {}'
Letter = namedtuple('Letter', 'name amount value')


def get_html():
    """Retrieve html from cache or URL"""
    if os.path.isfile(HTML):
        with open(HTML) as f:
            return f.read()
    return requests.get(URL).text


def get_table_rows(html):
    """Parse scrabble tile distribution into data structure
    Even lack of CSS selectors can be worked around :)
    Thanks SO - 23377533/python-beautifulsoup-parsing-table"""
    soup = Soup(html, 'html.parser')
    table = soup.find('table')
    table_body = table.find('tbody')
    return table_body.find_all('tr')


def get_distribution(rows):
    """Parse the table rows and convert them in a list of named tuples"""
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols[0] not in LETTERS:
            continue
        yield Letter(*cols)


if __name__ == "__main__":
    html = get_html()
    rows = get_table_rows(html)
    distribution = list(get_distribution(rows))
    total_amount = sum(int(letter.amount) for letter in distribution)

    assert total_amount == 98  # 100 - 2 blanks

    for letter in distribution:
        print(LETTER_REPR.format(*letter))
