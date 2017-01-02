from __future__ import print_function

import csv
import gensim
import utility
import sys

def interface(bowfname, tfidffname, ofname):

    tfidf = gensim.models.TfidfModel.load(
        utility.make_resource(tfidffname)
    )

    """Uses models trained in topic_maker_tfidf.py to set up data from our training data set
    from ./data/mxm_dataset_train.txt so it can be used in another sklearn model more easily"""

    filename = utility.make_resource(ofname)
    output_songs = []
    zeros = 0

    with open(filename, 'w') as out_file:

        with open(
                utility.make_resource(bowfname)
        ) as fd:
            for line in csv.reader(fd):

                # used to filter out songs without date data
                if line[0] == '0':
                    zeros += 1
                    continue

                song = map(lambda s: map(int, str.split(s, ':')), line[3:])
                song_tfidf = tfidf[song]
                # song_lsi_vec = lsi[song_tfidf]
                date_class = (int(line[0]) - 1900) // 10

                topic_vec = ['{}:{}'.format(item[0], (item[1])) for item in song_tfidf]

                print(','.join([line[0], str(date_class), ','.join(topic_vec)]), file=out_file)

    print("total num of missing dates: {}".format(zeros))
    # missing 62428 dates from song meta_data


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        bowfname, tfidffname, ofname = sys.argv[1], sys.argv[2], sys.argv[3]
    except:
        print("usage: {}  <bowfname> <tfidf-fname> <ofname>".format(sys.argv[0]))
        sys.exit(1)
    interface(bowfname, tfidffname, ofname)


if __name__ == '__main__':
    cli_interface()


