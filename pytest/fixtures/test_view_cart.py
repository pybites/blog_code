import re

import pytest

from groceries import Groceries


def test_initial_empty_cart():
    """Note no fixture here to test an empty cart creation"""
    cart = Groceries()
    assert len(cart) == 0
    assert cart.due == 0


def test_initial_filled_cart(cart):
    # thanks to __getitem__ can index the cart
    assert cart[0].product == 'celery'
    assert cart[0].price == 1
    assert cart[-1].product == 'pizza'
    assert cart[-1].price == 4

    assert len(cart) == 6
    assert cart.due == 22
    assert not cart.num_cravings_reached


@pytest.mark.parametrize("test_input,expected", [
    ('banana', 0),
    ('water', 1),
    ('Apples', 1),
    ('apple', 1),
    ('le', 2),
    ('zZ', 1),
    ('e', 5),
])
def test_search_item(cart, test_input, expected):
    assert len(list(cart.search(test_input))) == expected


def test_show_items(cart, capfd):
    cart.show()
    output = [line for line in capfd.readouterr()[0].split('\n')
              if line.strip()]

    assert re.search(r'^celery.*1$', output[0])
    assert re.search(r'^pizza \(craving\).*4$', output[5])
    assert re.search(r'^Total.*22$', output[-1])
