from functools import wraps
import time

def sleep(seconds=None):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Sleeping for {} seconds'.format(seconds))
            time.sleep(seconds if seconds else 1)
            return func(*args, **kwargs)
        return wrapper
    return real_decorator


if __name__ == '__main__':

    @sleep(1)  # @sleep without arg fails
    def hello():
        print('hello world')

    for _ in range(3):
        hello()
