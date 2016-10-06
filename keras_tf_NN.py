
import csv
from keras import backend as K
from keras.layers import Dense 
from keras.objectives import categorical_crossentropy 
from keras.metrics import categorical_accuracy as accuracy

import numpy as np 
import tensorflow as tf

# -----------------------------------------------------------------------------------
# data setup 
song_data = []

with open("./data/full_output_tfidf.csv") as fd:
    for line in csv.reader(fd):    
        document = map(lambda s: map(float, str.split(s, ':')), line[3:])
        
        X = [item[1] for item in document]

        # onehot encoding for categories 
        eye = np.eye(10)
        y = eye[int(line[2]) - 2]

        song_data.append([X, y])

song_data = np.array(song_data)

# spliting train/test 
train_data = song_data[:123200]
test_data = song_data[123200:]

# chunks traing data into blocks of 50 examples for training of model 
def chunker(data, size):
    return ([data[pos:pos + size] for pos in xrange(0, len(data), size)])

train_data_50 = chunker(train_data, 50)

# -----------------------------------------------------------------------------------
# starts tensorflow session with keras backend
sess = tf.Session()
K.set_session(sess)

# sets up placeholder so we can feed it to our model with our examples later 
songs = tf.placeholder(tf.float32, [None, 50])

# Keras layers that get called on by tensorflow tensors: 
x = Dense(30, activation='relu')(songs)
x = Dense(30, activation='relu')(x)
preds = Dense(10, activation='softmax')(x) # output layer 

labels = tf.placeholder(tf.float32, shape=(None, 10))

loss = tf.reduce_mean(categorical_crossentropy(labels, preds))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

with sess.as_default():
    for idx in range(10):
        block = train_data_50[idx]

        batch_xs = [part[0] for part in block]
        batch_ys = [part[1] for part in block]

        train_step.run(feed_dict={songs: batch_xs,
                                  labels: batch_ys})

# -----------------------------------------------------------------------------------

acc_value = accuracy(labels, preds)
with sess.as_default():
    test_block = test_data[-1000:] 

    batch_xs = [part[0] for part in test_block]
    batch_ys = [part[1] for part in test_block]

    print(acc_value.eval(feed_dict={songs: batch_xs,
                                  labels: batch_ys}))




