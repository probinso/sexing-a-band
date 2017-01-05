from __future__ import division, print_function

import csv
from collections import defaultdict
import numpy as np

from scipy.sparse import lil_matrix
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals   import joblib

import pickle
import utility
import sys

from imblearn.over_sampling import RandomOverSampler


def get_data(song_file):
    """grab data from csv and break into [X, y] list items"""

    song_data = []
    with open(utility.make_resource(song_file)) as fd:
        song_dict = defaultdict(int)
        count = 0

        for line in csv.reader(fd):
            song_vector = line[2:]
            song_decade = line[1]

            document = [item.split(':') for item in song_vector]
            X = dict([[int(item[0]), float(item[1])] for item in document])

            song_dict[int(song_decade)] += 1

            # filtering out songs from 20s & 30s & 40s
            if int(song_decade) <= 4:
                count += 1
                continue

            # subracting by 5 to move songs from 50s to zero index
            y = int(song_decade) - 5

            song_data.append([X, y])

        print("count of songs from 20s, 30s, 40s: {}".format(count))
        print("dict of num of song count by decade: {}".format(song_dict))

    return song_data


def chunker(data, size):
    """chunk data into 50 element lists for batch training"""
    return ([data[pos:pos + size] for pos in range(0, len(data), size)])


def oversample_data(data, dict_length):
    """helper func to oversample data"""
    ros = RandomOverSampler(random_state=42)

    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    new = matrix_func(X_data, dict_length)

    X_res, y_res = ros.fit_sample(new.toarray(), y_data)
    print('length after over_sampling! new_X: {}, new_y: {}'.format(X_res.shape, y_res.shape))

    return X_res, y_res


def sans_oversampling(data, dict_length):
    """helper func for non oversampled data"""

    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    X_new = matrix_func(X_data, dict_length)

    return X_new, y_data


def matrix_func(a_list, dict_length):
    """take a list of dicts and return a sparse lil_matrix"""
    # make a matrix that matches the size of list of dicts
    sparse_matrix = lil_matrix((len(a_list), dict_length))

    # loop through each dict in list, and add that dicts values to idx of key in sparse matrix
    for idx, a_dict in enumerate(a_list):
        for key in a_dict.keys():
            # subtracting 1 from the key because values for words in dict start at 1
            sparse_matrix[idx, key - 1] = a_dict[key]

    return sparse_matrix


def run_NB(train_data_50, dict_length, clf):
    """runs NB on chuncked data using partial_fit"""

    classes = range(7)
    for idx in range(len(train_data_50)):
        data = train_data_50[idx]

        # X_res, y_res = oversample_data(data, dict_length)
        X_res, y_res = sans_oversampling(data, dict_length)

        clf.partial_fit(X_res, y_res, classes)

    print("NB model finsihed training")
    return


def score(test_data):
    """score trained model, look at results within +/- 1 decade range"""

    # X_res, y_res = oversample_data(test_data)
    X_res, y_res = sans_oversampling(test_data)

    score = clf.score(X_res, y_res)

    predictions_dict = defaultdict(int)
    correct_range_pred = 0
    # look at individual prediciton of model wihtin a range and build result dict
    for idx, item in enumerate(X_res):
        model_out = clf.predict(item)

        # remember that 50s is starting decade when looking at results
        predictions_dict[model_out[0]] += 1

        prediciton_in_range1 = abs(y_res[idx] - model_out[0])
        if int(prediciton_in_range1) < 2:
            correct_range_pred += 1

    predict_percent = correct_range_pred / X_res.shape[0]
    print("percent correct_pred within +/- 1 decade block {}".format(predict_percent))
    print("score of NB model: {}".format(score))
    print("dict of decades predicted: {}".format(predictions_dict))
    return


def interface(ifname, dict_pickle, ofname):

    # get length of dict_pickle
    with open(utility.make_resource(dict_pickle), 'rb') as pf:
        lookup_dict = pickle.load(pf)
        dict_length = len(lookup_dict)
    print("length of lookup dict: {}".format(dict_length))

    song_data = get_data(ifname)

    # *** train/test split not being used with current data ***
    # spliting train/test
    # split_num = int(len(song_data) * .75)
    # train_data = song_data[:split_num]
    # test_data = song_data[split_num:]

    # chunk data into an array of 50 long examples
    train_data_50 = chunker(song_data, 50)

    # make instance of NB model
    clf = MultinomialNB(fit_prior=True)

    # train NB using partial fit
    run_NB(train_data_50, dict_length, clf)

    # *** training only currently, using mxm data to score elsewhere ***
    # score the model using test data
    #score(test_data)

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
