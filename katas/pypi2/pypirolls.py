import datetime
import ssl
import time
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

GOAL = 100000
TIMEOUT = 5 * 60 * 60

client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi',
                               context=ssl._create_unverified_context())

while True:
    now = datetime.datetime.now()
    packages = client.list_packages()
    num_packages = len(packages)
    print('It is {} and PyPI has {} packages'.format(now, num_packages))
    if num_packages >= GOAL:
        print('Reached goal!')
        break
    time.sleep(TIMEOUT)
