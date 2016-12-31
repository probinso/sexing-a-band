from __future__ import division

import csv
from collections import defaultdict
import numpy as np

from scipy.sparse import lil_matrix
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals   import joblib

import pickle
import utility

from imblearn.over_sampling import RandomOverSampler


def get_data():
    """grab data from csv and break into [X, y] list items"""

    song_data = []
    with open(utility.make_resource('only_tfidf.csv')) as fd:
        song_dict = defaultdict(int)
        count = 0

        for line in csv.reader(fd):
            song_vector = line[2:]
            song_decade = line[1]

            document = [item.split(':') for item in song_vector]
            X = dict([[int(item[0]), float(item[1])] for item in song_vector])

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


def oversample_data(data):
    """helper func to oversample data"""
    ros = RandomOverSampler(random_state=42)

    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    new = matrix_func(X_data)

    X_res, y_res = ros.fit_sample(new.toarray(), y_data)
    print('length after over_sampling! new_X: {}, new_y: {}'.format(X_res.shape, y_res.shape))

    return X_res, y_res


def sans_oversampling(data):
    """helper func for non oversampled data"""

    X_data = [item[0] for item in data]
    y_data = np.array([item[1] for item in data])

    X_new = matrix_func(X_data)

    return X_new, y_data


def matrix_func(a_list):
    """take a list of dicts and return a sparse lil_matrix"""
    # make a matrix that matches the size of list of dicts
    sparse_matrix = lil_matrix((len(a_list), 50000))

    # loop through each dict in list, and add that dicts values to idx of key in sparse matrix
    for idx, a_dict in enumerate(a_list):
        for key in a_dict.keys():
            # subtracting 1 from the key because values for words in dict start at 1
            sparse_matrix[idx, key - 1] = a_dict[key]

    return sparse_matrix


def run_NB(train_data_50):
    """runs NB on chuncked data using partial_fit"""

    classes = range(7)
    for idx in range(len(train_data_50)):
        data = train_data_50[idx]

        # X_res, y_res = oversample_data(data)
        X_res, y_res = sans_oversampling(data)

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
    print("score of NB model: {}".format(score)
    print("dict of decades predicted: {}".format(predictions_dict))
    return

if __name__ == '__main__':
    # get song data from csv
    song_data = get_data()

    # spliting train/test
    split_num = int(len(song_data) * .75)

    train_data = song_data[:split_num]
    test_data = song_data[split_num:]

    # chunk data into an array of 50 long examples
    train_data_50 = chunker(train_data, 50)

    # setup global NB model
    clf = MultinomialNB(fit_prior=True)

    # train NB using partial fit
    run_NB(train_data_50)

    # score the model using test data
    score(test_data)

    # dump model into a pickle file
    #pickle.dump(clf, open('./data/NB_pickle_pickle.pkl', 'wb'))
