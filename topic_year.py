from __future__ import print_function

import gensim
import csv

print(gensim.__file__)

from constants import DUMP_SIZE

lsi = gensim.models.LsiModel.load('./song_topics.lsi')

with open('./data/mxm_dataset_train.txt') as fd:
    line = '#'
    it = iter(fd)
    while line[0] == '#':
        line = next(it)

    raw = list(enumerate(line[1:].strip().split(','),1))

dump, keep = raw[:DUMP_SIZE], raw[DUMP_SIZE:]

lookup = {k - DUMP_SIZE : v for k, v in keep}
invert = {value:key for key, value in lookup.items()}

"""
create topic model
test document wrt topic and histogram on year
"""
from collections import defaultdict
d = defaultdict(list)
with open("./data/output.csv") as fd:
    for line in csv.reader(fd):
        year = line[1]
        _ = map(lambda s: map(int, str.split(s, ':')), line[2:])
        document = filter(lambda x : x[0] < DUMP_SIZE + 1, _)

        topics = sorted(lsi[document], key=lambda x: x[1], reverse=True)[:10]
        for t in topics:
            d[year].append(t[0])

for i in sorted(d):
    print(i)
    print("  ", sorted(d[i]))
    print()
