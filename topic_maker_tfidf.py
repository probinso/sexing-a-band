from __future__ import print_function

import csv
import gensim

with open('./data/mxm_dataset_train.txt') as fd:
    line = '#'
    it = iter(fd)
    while line[0] == '#':
        line = next(it)

    raw = list(enumerate(line[1:].strip().split(','),1))

lookup = {k : v for k, v in raw}

# ---------------------------------------------------------------

corpus = []
with open("./data/output.csv") as fd:
    for line in csv.reader(fd):
        document = map(lambda s: map(int, str.split(s, ':')), line[2:])

        corpus.append(document)

tfidf_model = gensim.models.TfidfModel(corpus, normalize=True)
tfidf_model.save("./tfidf_model.tfidf")

tfidf_corpus = []
for item in corpus: 
    tfidf_corpus.append(tfidf_model[item])
    
lsi = gensim.models.lsimodel.LsiModel(tfidf_corpus, num_topics=50, id2word=lookup)
for index, topic in lsi.print_topics(num_topics=10, num_words = 3):
    print(index)
    print("  " + topic)

lsi.save('./data/song_topics_tfidif.lsi')
