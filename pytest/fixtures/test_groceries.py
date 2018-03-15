import re

import pytest

from groceries import (Groceries, Item, DuplicateProduct,
                       MaxCravingsReached)


def _setup_items():
    products = 'celery apples water coffee chicken pizza'.split()
    prices = [1, 4, 2, 5, 6, 4]
    cravings = False, False, False, False, False, True
    for item in zip(products, prices, cravings):
        yield Item(*item)


def test_initial_empty_cart():
    cart = Groceries()

    assert len(cart) == 0
    assert cart.total_price == 0


def test_initial_filled_cart():
    items = list(_setup_items())
    cart = Groceries(items=items)

    # thanks to __getitem__ can index the cart
    assert cart[0].product == 'celery'
    assert cart[0].price == 1
    assert cart[-1].product == 'pizza'
    assert cart[-1].price == 4

    assert len(cart) == 6
    assert cart.total_price == 22
    assert not cart.num_cravings_reached


def test_add_item():
    items = list(_setup_items())
    cart = Groceries(items=items)

    oranges = Item(product='oranges', price=3, craving=False)
    cart.add(oranges)

    assert len(cart) == 7
    assert cart[-1].product == 'oranges'
    assert cart[-1].price == 3
    assert cart.total_price == 25
    assert not cart.num_cravings_reached


def test_add_item_duplicate():
    items = list(_setup_items())
    cart = Groceries(items=items)

    apples = Item(product='apples', price=4, craving=False)
    with pytest.raises(DuplicateProduct):
        cart.add(apples)


def test_add_item_max_cravings():
    items = list(_setup_items())
    cart = Groceries(items=items)

    chocolate = Item(product='chocolate', price=2, craving=True)
    cart.add(chocolate)
    assert cart.num_cravings_reached

    croissants = Item(product='croissants', price=3, craving=True)
    with pytest.raises(MaxCravingsReached):
        cart.add(croissants)  # wait till next week!


def test_delete_item():
    items = list(_setup_items())
    cart = Groceries(items=items)

    # not in collection
    croissant = 'croissant'
    with pytest.raises(IndexError):
        cart.delete(croissant)

    # in collection
    assert len(cart) == 6
    apples = 'apples'
    cart.delete(apples)
    # new product at this index
    assert len(cart) == 5
    assert cart[1].product == 'water'


@pytest.mark.parametrize("test_input,expected", [
    ('banana', 0),
    ('water', 1),
    ('Apples', 1),
    ('apple', 1),
    ('le', 2),
    ('zZ', 1),
    ('e', 5),
])
def test_search_item(test_input, expected):
    items = list(_setup_items())
    cart = Groceries(items=items)

    assert len(list(cart.search(test_input))) == expected


def test_show_items(capfd):
    items = list(_setup_items())
    cart = Groceries(items=items)

    cart.show()
    output = [line for line in capfd.readouterr()[0].split('\n')
              if line.strip()]

    assert re.search(r'^celery.*1$', output[0])
    assert re.search(r'^pizza \(craving\).*4$', output[5])
    assert re.search(r'^Total.*22$', output[-1])
