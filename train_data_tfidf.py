from __future__ import print_function

import csv
import gensim

tfidf = gensim.models.TfidfModel.load("./tfidf_model.tfidf")
lsi = gensim.models.LsiModel.load('./data/song_topics_tfidif.lsi')

"""Uses models trained in topic_maker_tfidf.py to set up data from our training data set 
    from ./data/mxm_dataset_train.txt so it can be used in another sklearn model more easily"""

filename = 'data/output_tfidf.csv'
output_songs = []

with open(filename, 'w') as out_file:

    with open("./data/output.csv") as fd:
        for line in csv.reader(fd):
            song = map(lambda s: map(int, str.split(s, ':')), line[2:])
            song_tfidf = tfidf[song]
            song_lsi_vec = lsi[song_tfidf]
            date_class = (int(line[1]) - 1900) // 10

            topic_vec = ['{}:{}'.format(item[0], item[1]) for item in song_lsi_vec]

            print(','.join([line[0], line[1], str(date_class), ','.join(topic_vec)]), file=out_file)
 
        