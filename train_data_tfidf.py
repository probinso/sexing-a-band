import csv
import gensim

tfidf = gensim.models.TfidfModel.load("./tfidf_model.tfidf")
lsi = gensim.models.LsiModel.load('./data/song_topics_tfidif.lsi')

"""Uses models trained in topic_maker_tfidf.py to set up data from our training data set 
    from ./data/mxm_dataset_train.txt so it can be used in another sklearn model more easily"""

filename = 'data/output_tfidf.csv'
output_songs = []

with open(filename, 'w') as out_file:
    writer = csv.writer(out_file)

    with open("./data/output.csv") as fd:
        for line in csv.reader(fd):
            song = map(lambda s: map(int, str.split(s, ':')), line[2:])
            song_tfidf = tfidf[song]
            song_lsi_vec = lsi[song_tfidf]
            date_class = (int(line[1]) - 1900) // 10

            output_songs.append([line[0], line[1], date_class, song_lsi_vec])

    writer.writerows(output_songs)

# This took quite a while to run and has a list of tuples converted to a string as the last value
# for each song. I'm wondering if there is a better/faster format to write it to a csv. 
        