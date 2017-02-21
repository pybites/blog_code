from collections import Counter
import sys

try:
    subscriber_file = sys.argv[1]
except IndexError:
    sys.exit('provide filename')

try:
    with open(subscriber_file) as f:
        lines = f.readlines()
except IOError:
    sys.exit('file not present')

stats = Counter(line.rstrip().split(',')[-1] for line in lines[1:])

for url, count in stats.most_common():
    print('{:<4} {}'.format(count, url))
