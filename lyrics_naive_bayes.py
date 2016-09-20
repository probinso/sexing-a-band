import csv
from collections import defaultdict

from sklearn.naive_bayes import GaussianNB

import numpy as np
from sklearn.cross_validation import train_test_split

X = []
y = []

with open("./data/output_tfidf.csv") as fd:
    for line in csv.reader(fd):    
        document = map(lambda s: map(float, str.split(s, ':')), line[3:])

        X.append([item[1] for item in document])
        y.append(line[2])

print len(X)
print len(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = GaussianNB()
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)

print score 

#-----------------------------------------------------------------------------
# looking at distrobution of decades in data 

# decades = defaultdict(int)

# for year in y:
#     decades[year] += 1

# print(decades.items()) 

# output from above: 
#[('11', 1391), ('10', 84769), ('3', 39), ('2', 37), ('5', 624), ('4', 73), 
#('7', 7965), ('6', 3235), ('9', 39516), ('8', 15178)]

# 152827 
#-----------------------------------------------------------------------------

