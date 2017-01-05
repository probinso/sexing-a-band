from __future__ import division, print_function

import csv
from collections import defaultdict
import numpy as np

from scipy.sparse import lil_matrix
from sklearn.naive_bayes import MultinomialNB

import pickle
import utility
import sys


def get_data(song_file):
    """grab data from csv and break into [X, y] list items"""

    song_data = []
    with open(utility.make_resource(song_file)) as fd:

        for line in csv.reader(fd):
            song_vector = line[2:]
            song_decade = line[1]

            document = [item.split(':') for item in song_vector]
            X = dict([[int(item[0]), float(item[1])] for item in document])

            # subtracting by 2 to move songs from 20s to zero idx
            y = int(song_decade) - 2

            song_data.append([X, y])

    return song_data


def data_prep(data, dict_length):
    """helper func that turns list of lists in format [[dict, year], ...]
       into [sparse_matrices] [year] format for training NB model"""

    # make a list of list matrix that matches the size of list of dicts
    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    # make a list of list matrix that matches the size of list of dicts
    lil_sparse_matrix = lil_matrix((len(X_data), dict_length))

    # loop through each dict in list, add dicts' values to correct idx in sparse matrix
    for idx, a_dict in enumerate(X_data):
        for key in a_dict.keys():
            # subtracting 1 from the key because values for words in dict start at 1
            lil_sparse_matrix[idx, key - 1] = a_dict[key]

    return lil_sparse_matrix, y_data


def run_NB(song_data, dict_length, clf):
    """runs NB on chuncked data using partial_fit"""

    # need to turn dicts in song_data into sparse matrices
    X_res, y_res = data_prep(song_data, dict_length)

    clf.fit(X_res, y_res)

    print("NB model finsihed training")
    return


def interface(ifname, dict_pickle, ofname):

    # get length of dict_pickle
    with open(utility.make_resource(dict_pickle), 'rb') as pf:
        lookup_dict = pickle.load(pf)
        dict_length = len(lookup_dict)
    print("length of lookup dict: {}".format(dict_length))

    # returns a list of lists, [[a dict of song vector, song decade]]
    song_data = get_data(ifname)

    # setup global NB model
    clf = MultinomialNB(fit_prior=True)

    # train NB using partial fit
    run_NB(song_data, dict_length, clf)

    # dump model into a pickle file
    pickle.dump(clf, open(utility.make_resource(ofname), 'wb'))


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        ifname, dict_pickle, ofname = sys.argv[1], sys.argv[2], sys.argv[3]
    except:
        print("usage: {}  <inpath> <outpath>".format(sys.argv[0]))
        sys.exit(1)
    interface(ifname, dict_pickle, ofname)


if __name__ == '__main__':
    cli_interface()
