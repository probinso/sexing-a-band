import csv
from collections import defaultdict

#from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier


import numpy as np
from sklearn.cross_validation import train_test_split

X = []
y = []

with open("./data/full_output_tfidf.csv") as fd:
    for line in csv.reader(fd):    
        document = map(lambda s: map(float, str.split(s, ':')), line[3:])

        X.append([item[1] for item in document])
        y.append(line[2])

print('num of data samples: {}'.format(len(X)))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=5)

# clf = MultinomialNB(fit_prior=True)
# clf.fit(X_train, y_train)

# score = clf.score(X_test, y_test)

# print("NB score: {}".format(score))

t_samples = 175234
class_prob = {'11': 1592/t_samples, '10': 98614/t_samples, '3': 40/t_samples, '2': 38/t_samples,
    '5': 711/t_samples, '4': 75/t_samples, '7': 8784/t_samples, '6': 3464/t_samples, 
    '9': 44913/t_samples, '8': 17003/t_samples}


forest = RandomForestClassifier(n_estimators=10, min_samples_leaf=10, random_state=50, class_weight=class_prob)
forest.fit(X_train, y_train)

forest_score = forest.score(X_test, y_test)

print("forest score: {}".format(forest_score))


#-----------------------------------------------------------------------------
# looking at distrobution of decades in data 

# decades = defaultdict(int)

# for year in y:
#     decades[year] += 1

# print(decades.items()) 

# output from above: 
# [('11', 1592), ('10', 98614), ('3', 40), ('2', 38), ('5', 711), ('4', 75), 
# ('7', 8784), ('6', 3464), ('9', 44913), ('8', 17003)]

# 175234 - total samples  

#Dict of class wieghts 
# class_prob = {'11': 1592/t_samples, '10': 98614/t_samples, '3': 40/t_samples, '2': 38/t_samples,
#     '5': 711/t_samples, '4': 75/t_samples, '7': 8784/t_samples, '6': 3464/t_samples, 
#     '9': 44913/t_samples, '8': 17003/t_samples}
#-----------------------------------------------------------------------------

