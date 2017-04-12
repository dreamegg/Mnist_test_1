import matplotlib.pyplot as plt
import random

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

tf.set_random_seed(777)

mnist = input_data.read_data_sets("./MNIST_data/", one_hot=True)

nb_class = 10

X= tf.placeholder(tf.float32, [None, 28*28])
Y=tf. placeholder(tf.float32, [None, nb_class])

W = tf.Variable(tf.random_normal([28*28, nb_class]))
b = tf.Variable(tf.random_normal([nb_class]))

hypo = tf.nn.softmax(tf.matmul(X, W)+b)
cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(hypo), axis=1))
opti = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

is_correct = tf.equal(tf.arg_max(hypo,1), tf.arg_max(Y,1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

train_epoch = 1000
batch_size =100

with tf.Session() as sess :
    sess.run(tf.global_variables_initializer())

    for epoch in range(train_epoch):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples / batch_size)

        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            c, _ = sess.run([cost, opti], feed_dict = {X:batch_xs, Y:batch_ys})
            avg_cost += c/total_batch

        print ("Epoch : ", "%04d" % (epoch+1), 'cost =', '{:.9f}'.format(avg_cost))
        print("Accuracy: ", accuracy.eval(session=sess, feed_dict={X: mnist.test.images, Y: mnist.test.labels}))

    r = random.randint(0, mnist.test.num_examples - 1)
    print("Label:", sess.run(tf.argmax(mnist.test.labels[r:r+1], 1)))
    print("Prediction:", sess.run(tf.argmax(hypo, 1), feed_dict={X: mnist.test.images[r:r + 1]}))

    plt.imshow(mnist.test.images[r:r + 1].reshape(28, 28), cmap='Greys', interpolation='nearest')
    plt.show()