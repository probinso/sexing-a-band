from __future__ import print_function

import csv
import gensim

tfidf = gensim.models.TfidfModel.load("./full_tfidf_model.tfidf")

def tfidf_csv_writer():

    """Writing each songs tfidf score to an output csv for training """

    filename = 'data/only_tfidf_output.csv'
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
                date_class = (int(line[2]) - 1900) // 10

                topic_vec = ['{}:{}'.format(item[0], (item[1])) for item in song_tfidf]

                print(','.join([line[0], line[2], str(date_class), ','.join(topic_vec)]), file=out_file)
 
if __name__ == '__main__':
    tfidf_csv_writer()