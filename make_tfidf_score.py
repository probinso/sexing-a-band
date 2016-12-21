from __future__ import print_function

import csv
import gensim

tfidf = gensim.models.TfidfModel.load("./full_tfidf_model.tfidf")
# lsi = gensim.models.LsiModel.load('./data/full_song_topics_tfidif.lsi')

"""Uses models trained in topic_maker_tfidf.py to set up data from our training data set 
    from ./data/mxm_dataset_train.txt so it can be used in another sklearn model more easily"""

filename = 'data/only_tfidf.csv'
output_songs = []
zeros = 0

with open(filename, 'w') as out_file:

    with open("./data/full_output.csv") as fd:
        for line in csv.reader(fd):

            # used to filter out songs without date data 
            if line[2] == '0':
                zeros += 1 
                continue 

            song = map(lambda s: map(int, str.split(s, ':')), line[3:])
            song_tfidf = tfidf[song]
            # song_lsi_vec = lsi[song_tfidf]
            date_class = (int(line[2]) - 1900) // 10

            topic_vec = ['{}:{}'.format(item[0], (item[1])) for item in song_tfidf]

            print(','.join([line[0], line[2], str(date_class), ','.join(topic_vec)]), file=out_file)
 
print("total num of missing dates: {}".format(zeros))
# missing 62428 dates from song meta_data 