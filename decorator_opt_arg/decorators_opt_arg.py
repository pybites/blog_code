from functools import wraps, partial
import time

def sleep(func=None, *, seconds=None, msg=None):
    if func is None:
        return partial(sleep, seconds=seconds, msg=msg)

    seconds = seconds if seconds else 1
    msg = msg if msg else 'Sleeping for {} seconds'.format(seconds)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        time.sleep(seconds)
        return func(*args, **kwargs)
    return wrapper


if __name__ == '__main__':

    def call_n_times(func, n=3):
        for _ in range(n):
            func()

    @sleep  # works now!
    def hello():
        print('hello world')

    print('\nWithout args\n---')
    call_n_times(hello)


    @sleep(seconds=2)
    def hello():
        print('hello world')

    print('\nWith one opt arg: seconds\n---')
    call_n_times(hello)


    @sleep(seconds=1, msg='I work so hard, resting a bit')
    def hello():
        print('hello world')

    print('\nWith two opt args: seconds and msg\n---')
    call_n_times(hello)
