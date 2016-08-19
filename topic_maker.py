from __future__ import print_function

import csv
import gensim

fd = open('./data/mxm_dataset_train.txt')
line = '#'
it = iter(fd)
while line[0] == '#':
    line = next(it)

DUMP_SIZE = 1000

raw = list(enumerate(line[1:].strip().split(','),1))
# original = {value: key for key, value in raw}
dump, keep = raw[:DUMP_SIZE], raw[DUMP_SIZE:]

lookup = {k - DUMP_SIZE : v for k, v in keep}
invert = {value:key for key, value in lookup.items()}

"""
create topic model
test document wrt topic and histogram on year
"""

corpus = []
with open("./data/output.csv"):
    for line in csv.reader(fd):
        document = map(lambda s: map(int, str.split(s, ':')), line[2:])

        corpus.append(filter(lambda x : x[0] < DUMP_SIZE + 1, document))

lsi = gensim.models.lsimodel.LsiModel(corpus, num_topics=900, id2word=lookup)
for index, topic in lsi.print_topics(num_topics=10, num_words = 3):
    print(index)
    print("  " + topic)

