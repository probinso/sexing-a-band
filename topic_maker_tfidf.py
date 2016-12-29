from __future__ import print_function

import csv
import gensim
import utility


corpus = []
with open(utility.make_resource('bow_english.csv')) as fd:
    it = iter(fd)
    next(it) # skip ordered word lookup line
    for line in csv.reader(it):
        document = list(map(lambda s: map(int, str.split(s, ':')), line[3:]))

        corpus.append(document)

tfidf_model = gensim.models.TfidfModel(corpus, normalize=True)
tfidf_model.save(utility.make_resource('full_tfidf_model.tfidf'))
