from time import sleep

import pytest

from groceries import Groceries, Item


@pytest.fixture(scope="session")
def cart():
    """Setup code to create a groceries cart object with 6 items in it"""
    print('sleeping a bit at session level')
    sleep(1)  # for scope=module/session demo purposes
    products = 'celery apples water coffee chicken pizza'.split()
    prices = [1, 4, 2, 5, 6, 4]
    cravings = False, False, False, False, False, True

    items = []
    for item in zip(products, prices, cravings):
        items.append(Item(*item))

    return Groceries(items)
