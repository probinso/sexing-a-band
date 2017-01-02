from __future__ import print_function

import csv
import gensim
import utility

def interface(ifname, ofname):
    corpus = []
    with open(utility.make_resource(ifname)) as fd:
        it = iter(fd)
        next(it) # skip ordered word lookup line
        for line in csv.reader(it):
            document = list(map(lambda s: map(int, str.split(s, ':')), line[3:]))

            corpus.append(document)

    tfidf_model = gensim.models.TfidfModel(corpus, normalize=True)
    tfidf_model.save(utility.make_resource(ofname))


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        ifname, ofname = sys.argv[1], sys.argv[2]
    except:
        print("usage: {}  <ifname> <ofname>".format(sys.argv[0]))
        sys.exit(1)
    interface(ifname, ofname)


if __name__ == '__main__':
    cli_interface()
