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
import random

from imblearn.over_sampling import RandomOverSampler


def get_data(song_file):
    """grab data from csv and break into [X, y] list items where X is a dict
       that represents a song's vector and y is the category of that song"""

    # 1920 always starting zero index, bin size depends on bow_english_year

    song_data = []
    with open(utility.make_resource(song_file)) as fd:
        song_class_dict = defaultdict(int)
        song_year_dict = defaultdict(int)

        for line in csv.reader(fd):
            song_year = line[0]
            song_class = int(line[1])
            song_vector = line[2:]

            document = [item.split(':') for item in song_vector]
            X = dict([[int(item[0]), float(item[1])] for item in document])

            song_class_dict[int(song_class)] += 1

            # find year breakdown by song, remove later
            song_year_dict[int(song_year)] += 1

            song_data.append([X, song_class])

    return song_data, song_class_dict


def chunker(data, size):
    """chunk data into 50 element lists for batch training"""
    return ([data[pos:pos + size] for pos in range(0, len(data), size)])


def oversample_data(data):
    """helper func to oversample data"""
    ros = RandomOverSampler(random_state=42)

    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    print('length after over_sampling! new_X: {}, new_y: {}'.format(len(X_data), len(y_data)))

    return X_data, y_data


def sans_oversampling(data):
    """helper func for non oversampled data"""

    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    return X_data, y_data


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


def run_NB(train_data_50, clf, dict_length, target_classes, ovsmpl=False):
    """runs NB on chuncked data using partial_fit"""

    classes = [0,1,2,3,4,5,6,7,8]
    for idx in range(len(train_data_50)):
        data = train_data_50[idx]

        if ovsmpl:
            X_res, y_res = oversample_data(data)
        else:
            X_res, y_res = sans_oversampling(data)

        # make song vectors into lil matrix
        X_vec_matrix = matrix_func(X_res, dict_length)

        clf.partial_fit(X_vec_matrix, y_res, classes=classes)

    print("NB model finsihed training")
    return clf


def score(test_data, clf, dict_length, ovsmpl=False):
    """score trained model, look at results within +/- 1 decade range"""

    if ovsmpl:
        X_res, y_res = oversample_data(test_data)
    else:
        X_res, y_res = sans_oversampling(test_data)

    X_vec_matrix = matrix_func(X_res, dict_length)

    score = clf.score(X_vec_matrix, y_res)

    predictions_dict = defaultdict(int)
    correct_range_pred = 0
    # look at individual prediciton of model wihtin a range and build result dict
    for idx, item in enumerate(X_vec_matrix):

        model_out = clf.predict(item)

        # remember that 50s is starting decade when looking at results
        predictions_dict[model_out[0]] += 1

        prediciton_in_range1 = abs(y_res[idx] - model_out[0])
        if int(prediciton_in_range1) < 2:
            correct_range_pred += 1

    predict_percent = correct_range_pred / X_vec_matrix.shape[0]
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

    song_data, song_class_dict = get_data(ifname)
    target_classes_len = len(song_class_dict)

    random.shuffle(song_data)

    split_num = int(len(song_data) * .75)
    #print("split num in interface: {}".format(split_num))
    train_data = song_data[:split_num]
    test_data = song_data[split_num:]

    # chunk data into an array of 50 long examples
    train_data_50 = chunker(train_data, 50)

    # make instance of NB model
    clf = MultinomialNB(fit_prior=True)

    # train NB using partial fit
    # add a 4th optional arg to oversample: T/F flag. False is default
    trained_clf = run_NB(train_data_50, clf, dict_length, target_classes_len, True)

    # score the model using test data
    # add a 4th optional arg to oversample: T/F flag. False is default
    score(test_data, trained_clf, dict_length, True)

    # dump model into a pickle file
    pickle.dump(trained_clf, open(utility.make_resource(ofname), 'wb'))


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
