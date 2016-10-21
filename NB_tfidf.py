import csv
from collections import defaultdict
import numpy as np 

from scipy.sparse import lil_matrix
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB

from imblearn.over_sampling import ADASYN


def get_data():
    """grab data from csv and break into [X, y] list items"""
    song_data = []
    with open("./data/only_tfidf.csv") as fd:
        for line in csv.reader(fd):
            # ********* might be a way to make this split/dict convertion better ********    
            document = [item.split(':') for item in line[3:]]
            X = dict([[int(item[0]), float(item[1])] for item in document])
            y = int(line[2]) - 2
            
            song_data.append([X, y])

    return song_data
 
def chunker(data, size):
    """chunk data into 50 element lists for batch training"""
    return ([data[pos:pos + size] for pos in xrange(0, len(data), size)])


def matrix_func(a_list):
    """take a list of dicts and return a sparse lil_matrix"""
    # make a matrix that matches the size of list of dicts 
    sparse_matrix = lil_matrix((len(a_list), 5000))

    # loop through each dict in list, and add that dicts values to idx of key in sparse matrix 
    for idx, a_dict in enumerate(a_list):

        for key in a_dict.keys(): 
            # subtracting 1 from the key because values in dict start at 1 
            sparse_matrix[idx, key - 1] = a_dict[key]
    
    return sparse_matrix

def run_NB(train_data_50):
    """runs NB on chuncked data using partial_fit"""
    classes = range(11)

    ada = ADASYN(random_state=42)

    for idx in range(len(train_data_50)):
        data = train_data_50[idx]

        X_data = [item[0] for item in data]
        y_data = np.array([item[1] for item in data])

        new = matrix_func(X_data)

        #print('length of X before resample: {}, length y: {}'.format(len(new), y_data.shape))
        X_res, y_res = ada.fit_sample(new.toarray(), y_data)
        X_res = matrix_func(X_res)

        print('length after over_sampling! new_X: {}, new_y: {}'.format(X_res.shape, y_res.shape))

        clf.partial_fit(X_res, y_res, classes=classes)


def score(test_data):
    """score the model being trained"""
    # need to break out test data same as above 
    X_test = [item[0] for item in test_data]
    y_test = [item[1] for item in test_data]

    new = matrix_func(X_test)

    score = clf.score(new, y_test)

    print("NB score: {}".format(score))

    # --------------------------------------------------
    # look at what values model is predicting 
    predictions = defaultdict(int)

    for item in new:
        model_out = clf.predict(item)
        predictions[model_out[0] + 2] += 1

    print(predictions)
    # --------------------------------------------------
    # results from above 
    # NB score: 0.566221235211
    # defaultdict(<type 'int'>, {8: 7, 9: 3491, 10: 48580, 5: 85, 7: 71})

    # --------------------------------------------------
    # predict the probabilites for each category being selected 
    for item in new:
        model_out = clf.predict_proba(item)
        print(model_out)
    # --------------------------------------------------


if __name__ == '__main__':
    # get song data from csv 
    song_data = get_data()

    # spliting train/test 
    train_data = song_data[:500]
    test_data = song_data[500:530]

    # chunk data into an array of 50 long examples  
    train_data_50 = chunker(train_data, 50)

    # setup global NB model 
    clf = MultinomialNB()
    # clf.set_params()

    # train NB using partial fit 
    run_NB(train_data_50)

    # score the model using test data
    score(test_data)






