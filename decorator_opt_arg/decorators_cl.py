from functools import wraps
import time

class sleep:

    def __init__(self, seconds=None):
        self.seconds = seconds if seconds else 1

    def __call__(self, func):
        wraps(func)(self)
        def wrapped_f(*args):
            print('Sleeping for {} seconds'.format(self.seconds))
            time.sleep(self.seconds)
            func(*args)
        return wrapped_f


if __name__ == '__main__':

    @sleep(1)  # @sleep without arg fails
    def hello():
        print('hello world')

    for _ in range(3):
        hello()
