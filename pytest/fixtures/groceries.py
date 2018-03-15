from collections import namedtuple

MAX_CRAVINGS = 2

Item = namedtuple('Item', 'product price craving')


class DuplicateProduct(Exception):
    pass


class MaxCravingsReached(Exception):
    pass


class Groceries:

    def __init__(self, items=None):
        """This cart can be instantiated with a list of namedtuple
           items, if not provided use an empty list"""
        self._items = items if items is not None else []

    def show(self):
        """Print a simple table of cart items with total at the end"""
        for item in self._items:
            product = f'{item.product}'
            if item.craving:
                product += ' (craving)'
            print(f'{product:<30} | {item.price:>3}')
        print('-' * 36)
        print(f'{"Total":<30} | {self.total_price:>3}')

    def add(self, new_item):
        """Add a new item to cart, raise exceptions if item already in
           cart, or when we exceed MAX_CRAVINGS"""
        if any(item for item in self if item.product == new_item.product):
            raise DuplicateProduct(f'{new_item.product} already in items')
        if new_item.craving and self.num_cravings_reached:
            raise MaxCravingsReached(f'{MAX_CRAVINGS} allowed')
        self._items.append(new_item)

    def delete(self, product):
        """Delete item matching 'product', raises IndexError
           if no item matches"""
        for i, item in enumerate(self):
            if item.product == product:
                self._items.pop(i)
                break
        else:
            raise IndexError(f'{product} not in cart')

    def search(self, search):
        """Case insensitive 'contains' search, this is a
           generator returning matching Item namedtuples"""
        for item in self:
            if search.lower() in item.product:
                yield item

    @property
    def total_price(self):
        """Calculate total price of cart"""
        return sum(item.price for item in self)

    @property
    def num_cravings_reached(self):
        """Calculate number of cravings in cart"""
        return len([item for item in self if item.craving]) >= MAX_CRAVINGS

    def __len__(self):
        """The len of cart"""
        return len(self._items)

    def __getitem__(self, index):
        """Making the class iterable (cart = Cart() -> cart[1] etc)
           without this dunder I would get 'TypeError: 'Cart' object does
           not support indexing' when trying to index it"""
        return self._items[index]
