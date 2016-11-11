from __future__ import print_function

import csv
import gensim


corpus = []
with open("./data/full_output.csv") as fd:
    for line in csv.reader(fd):
        document = map(lambda s: map(int, str.split(s, ':')), line[3:])

        corpus.append(document)

tfidf_model = gensim.models.TfidfModel(corpus, normalize=True)
tfidf_model.save("./full_tfidf_model.tfidf")
