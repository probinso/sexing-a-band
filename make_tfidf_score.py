from __future__ import print_function

import csv
import gensim
import utility
import sys

def interface(bowfname, tfidffname, ofname):

    tfidf = gensim.models.TfidfModel.load(
        utility.make_resource(tfidffname)
    )

    filename = utility.make_resource(ofname)

    with open(filename, 'w') as out_file:

        with open(utility.make_resource(bowfname)) as fd:
            for line in csv.reader(fd):
                # format of line: year, year_bin, song

                song = map(lambda s: map(int, str.split(s, ':')), line[2:])
                song_tfidf = tfidf[song]

                song_vec = ['{}:{}'.format(item[0], (item[1])) for item in song_tfidf]

                print(','.join([line[0], line[1], ','.join(song_vec)]), file=out_file)


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


