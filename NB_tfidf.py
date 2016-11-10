from __future__ import division 

import csv
from collections import defaultdict
import numpy as np 

from scipy.sparse import lil_matrix
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

import pickle

from imblearn.over_sampling import RandomOverSampler


def get_data():
    """grab data from csv and break into [X, y] list items"""
    song_data = []
    with open("./data/only_tfidf.csv") as fd:
        song_dict = defaultdict(int)
        count = 0
        for line in csv.reader(fd):
            # ********* might be a way to make this split/dict convertion better ********    
            document = [item.split(':') for item in line[3:]]
            X = dict([[int(item[0]), float(item[1])] for item in document])

            song_dict[int(line[2])] += 1

            # filtering out songs from 20s & 30s & 40s(153 songs total)
            if int(line[2]) <= 4:
                count += 1
                continue

            # subracting by 5 to move songs from 50s to zero index 
            y = int(line[2]) - 5

            song_data.append([X, y])

        print("count of songs from 20s, 30s, 40s: {}".format(count))
        print(song_dict)


    return song_data
 
def chunker(data, size):
    """chunk data into 50 element lists for batch training"""
    return ([data[pos:pos + size] for pos in xrange(0, len(data), size)])

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
    sparse_matrix = lil_matrix((len(a_list), 5000))

    # loop through each dict in list, and add that dicts values to idx of key in sparse matrix 
    for idx, a_dict in enumerate(a_list):

        for key in a_dict.keys(): 
            # subtracting 1 from the key because values for words in dict start at 1 
            sparse_matrix[idx, key - 1] = a_dict[key]
    
    return sparse_matrix

def run_NB(train_data_50):
    """runs NB on chuncked data using partial_fit"""

    classes = [0, 1, 2, 3, 4, 5, 6]

    for idx in range(len(train_data_50)):
        print("running NB in loop")
        data = train_data_50[idx]

        # X_res, y_res = oversample_data(data)

        X_res, y_res = sans_oversampling(data)

        clf.partial_fit(X_res, y_res, classes)

def score(test_data):
    """score the model being trained"""
    # oversample & break up data 
    # X_res, y_res = oversample_data(test_data)

    X_res, y_res = sans_oversampling(test_data)

    score = clf.score(X_res, y_res)

    print("NB score: {}".format(score))

    # --------------------------------------------------
    # look at what values model is predicting 
    predictions = defaultdict(int)

    correct_pred = 0
    for idx, item in enumerate(X_res):
        model_out = clf.predict(item)

        # adding 5 beacuse 50s is starting decade
        predictions[model_out[0]] += 1

        # --------------------------------------------------
        # counting number of predictions within correct range 

        prediciton_in_range1 = abs(y_res[idx] - model_out[0])
        print(type(prediciton_in_range1))
        print(prediciton_in_range1)

        
        if int(prediciton_in_range1) < 2:
            correct_pred += 1

        print(correct_pred)

    predict_percent = correct_pred / X_res.shape[0]
    print("correct_pred within 1 decade block {}".format(predict_percent))

    print('*' * 70)
    print(correct_pred)
    print(X_res.shape)
    print('*' * 70)

    print(predictions)
    print("NB score: {}".format(score))
    # # --------------------------------------------------
    # # results from above 
    # # NB score: 0.566221235211
    # # defaultdict(<type 'int'>, {8: 7, 9: 3491, 10: 48580, 5: 85, 7: 71})


if __name__ == '__main__':
    # get song data from csv 
    song_data = get_data()

    # spliting train/test 
    train_data = song_data[:140000]
    test_data = song_data[140000:150000]

    # chunk data into an array of 50 long examples  
    train_data_50 = chunker(train_data, 50)

    # setup global NB model 
    clf = MultinomialNB(fit_prior=True)

    # train NB using partial fit 
    run_NB(train_data_50)

    # score the model using test data
    score(test_data)

    # dump model into a pickle file 
    # with open('./data/NB_pickles.pkl', 'wb') as fo:
    #     joblib.dump(clf, fo)

    # with open('./data/NB_pickle_pickle.pkl', 'wb') as pf:

    pickle.dump(clf, open('./data/NB_pickle_pickle.pkl', 'wb'))






