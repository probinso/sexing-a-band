import csv
import numpy as np 

from scipy.sparse import coo_matrix
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB


def get_data():
    """grab data from csv and break into [X, y] list items"""
    song_data = []
    with open("./data/only_tfidf.csv") as fd:
        for line in csv.reader(fd):    
            # document = map(lambda s: map(float, str.split(s, ':')), line[3:])
            document = [item.split(':') for item in line[3:]]        
            X = [[int(item[0]), float(item[1])] for item in document]
            y = int(line[2]) - 2
            
            song_data.append([X, y])

    return song_data
 
def chunker(data, size):
    """chunk data into 50 element lists for batch training"""
    return ([data[pos:pos + size] for pos in xrange(0, len(data), size)])

# change to each column having a word value, transpose what you have 
def sparse_matrix(a_list):
    """take list of [idx, tfidf scores] and convert to a sparse matrix with zeros included"""
    row = np.array([item[0] for item in a_list])
    col = np.array([0 for _ in range(len(row))])
    data = np.array([item[1] for item in a_list])

    try:
        matrix = coo_matrix((data, (row, col)), shape=(5001,1)).toarray()
    except Exception:
        print(Exception)

    return matrix

def run_NB(train_data_50):
    """runs NB on chuncked data using partial_fit"""
    classes = range(11)

    for idx in range(len(train_data_50)):
        print("start loop")

        data = train_data_50[idx]

        X_data = [item[0] for item in data]
        print(X_data)
        y_data = np.array([item[1] for item in data])
        print(y_data.shape)
        
        # had to reshape 3d array to 2d 
        X_sparse = np.array(map(sparse_matrix, X_data))
        print(X_sparse.shape)
        new = X_sparse.reshape(50, 5001)

        print(new.shape)

        clf.partial_fit(new, y_data, classes=classes)


def score(test_data):
    # need to break out test data same as above 
    X_test = [item[0] for item in test_data]
    y_test = [item[1] for item in test_data]

    X_test_sparse = np.array(map(sparse_matrix, X_test))
    new = X_test_sparse.reshape(len(X_test_sparse), 5001)

    score = clf.score(new, y_test)

    print("NB score: {}".format(score))


if __name__ == '__main__':
    song_data = get_data()

    # spliting train/test 
    train_data = song_data[:500]
    test_data = song_data[500:550]

    # chunk data into an array of 50 long examples  
    train_data_50 = chunker(train_data, 50)

    # setup global NB model 
    clf = MultinomialNB(fit_prior=True)

    # train NB using partial fit 
    run_NB(train_data_50)

    # score the model using test data
    score(test_data)






