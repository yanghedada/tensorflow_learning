# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 16:23:02 2017

@author: YANG_HE
"""

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets(r'E:\python\mnist_data', one_hot=True)

import tensorflow as tf

# Parameters
learning_rate = 0.001
training_iters = 20
batch_size = 20
display_step = 2

# Network Parameters
n_input = 784 # MNIST data input (img shape: 28*28)
n_classes = 10 # MNIST total classes (0-9 digits)
dropout = 0.8 # Dropout, probability to keep units

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) # dropout (keep probability)


def dnn(_X, _weights, _biases, _dropout):
    # Reshape input picture
  

   
    _X = tf.nn.dropout(_X, _dropout)#//这里可以让dropout都不同 我就一样了
    d1 = tf.nn.relu(tf.nn.bias_add(tf.matmul(_X,_weights['wd1']),_biases['bd1']), name="d1")
  
    d2x = tf.nn.dropout(d1, _dropout)
    d2 =  tf.nn.relu(tf.nn.bias_add(tf.matmul(d2x,_weights['wd2']),_biases['bd2']), name="d2")
    
    #dense1 = tf.nn.relu(tf.matmul(dense1, _weights['wd1']) + _biases['bd1'], name='fc1') # Relu activation

    #dense2 = tf.nn.relu(tf.matmul(dense1, _weights['wd2']) + _biases['bd2'], name='fc2') # Relu activation
    dout =tf.nn.dropout(d2,_dropout)
    # Output, class prediction
    out = tf.matmul(dout, _weights['out']) + _biases['out']
    return out

# Store layers weight & bias
weights = {
    'wd1': tf.Variable(tf.random_normal([784,600], stddev=0.01)),
    'wd2': tf.Variable(tf.random_normal([600,480], stddev=0.01)),
    'out': tf.Variable(tf.random_normal([480, 10]))
}
biases = {
    'bd1': tf.Variable(tf.random_normal([600])),
    'bd2': tf.Variable(tf.random_normal([480])),
    'out': tf.Variable(tf.random_normal([10])),
}

# Construct model
pred = dnn(x, weights, biases, keep_prob)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph
with tf.Session() as sess:
    writer = tf.summary.FileWriter("cnn/logs", sess.graph)
    sess.run(init)

    step = 1
    # Keep training until reach max iterations
    while step * batch_size < training_iters:
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        # Fit training using batch data
        sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys, keep_prob: dropout})
        if step % display_step == 0:
            # Calculate batch accuracy
            acc = sess.run(accuracy, feed_dict={x: batch_xs, y: batch_ys, keep_prob: 1.})
            # Calculate batch loss
            loss = sess.run(cost, feed_dict={x: batch_xs, y: batch_ys, keep_prob: 1.})
            print ("Iter " + str(step*batch_size) + ", Minibatch Loss= " + "{:.6f}".format(loss) + ", Training Accuracy= " + "{:.5f}".format(acc))
            
        step += 1
    print ("Optimization Finished!")
    # Calculate accuracy for 256 mnist test images
    print ("Testing Accuracy:", sess.run(accuracy, feed_dict={x: mnist.test.images[:256], y: mnist.test.labels[:256], keep_prob: 1.}))

