from copy import deepcopy

import pytest

from groceries import Item, DuplicateProduct, MaxCravingsReached


def test_add_item(cart):
    cart = deepcopy(cart)  # not needed if scope=function

    oranges = Item(product='oranges', price=3, craving=False)
    cart.add(oranges)

    assert len(cart) == 7
    assert cart[-1].product == 'oranges'
    assert cart[-1].price == 3
    assert cart.due == 25
    assert not cart.num_cravings_reached


def test_add_item_max_cravings(cart):
    cart = deepcopy(cart)
    chocolate = Item(product='chocolate', price=2, craving=True)
    cart.add(chocolate)
    assert cart.num_cravings_reached

    croissants = Item(product='croissants', price=3, craving=True)
    with pytest.raises(MaxCravingsReached):
        cart.add(croissants)  # wait till next week!


def test_add_item_duplicate(cart):
    apples = Item(product='apples', price=4, craving=False)
    with pytest.raises(DuplicateProduct):
        cart.add(apples)


def test_delete_item(cart):
    cart = deepcopy(cart)
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
