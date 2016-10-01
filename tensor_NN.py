import csv 
import tensorflow as tf 
from sklearn.cross_validation import train_test_split
import numpy as np 

# -----------------------------------------------------------------------------------

# commands used to install TensorFlow: 
# export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0rc0-py2-none-any.whl
# pip install --upgrade $TF_BINARY_URL

# -----------------------------------------------------------------------------------

X = []
y = []

with open("./data/full_output_tfidf.csv") as fd:
    for line in csv.reader(fd):    
        document = map(lambda s: map(float, str.split(s, ':')), line[3:])

        X.append([item[1] for item in document])
        y.append(line[2]) 

X = np.array(X)
y = np.array(y)

# -----------------------------------------------------------------------------------
# transform our classification values into arrays where 1 marks class
eye = eye = np.eye(10)

y = [eye[int(item) - 2] for item in y]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=5)

# -----------------------------------------------------------------------------------

# sets up placeholder so we can feed it to our model with our examples later 
x = tf.placeholder(tf.float32, [None, 50])

# placeholder for wieghts and bias of NN intialized to zeros 
W = tf.Variable(tf.zeros([50, 10]))
b = tf.Variable(tf.zeros([10]))

# model setup equation 
y = tf.nn.softmax(tf.matmul(x, W) + b)

# placeholder for actual answers, used to calculate cross entropy 
y_ = tf.placeholder(tf.float32, [None, 10])

# calculate cross entropy of model, basically how bad model is 
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

# performs backprop on model 
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# intializes all the elements we declated above 
init = tf.initialize_all_variables()

# starts tensor flow session  
sess = tf.Session()
sess.run(init)

#  
for i in range(1000):
  batch_xs = X_train
  batch_ys = y_train
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# test accuracy of model 
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print("running")
print(sess.run(accuracy, feed_dict={x: X_test,
                                      y_: y_test}))















