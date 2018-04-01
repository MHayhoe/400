from __future__ import absolute_import, division, print_function

import os
import matplotlib as plt
import tensorflow as tf
import numpy as np
import tensorflow.contrib.eager as tfe

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#tf.enable_eager_execution()
#tf.contrib.eager.Variable
print("TensorFlow version: {}".format(tf.VERSION))
print("Eager execution: {}".format(tf.executing_eagerly()))
train_dataset_url = "http://download.tensorflow.org/data/iris_training.csv"

train_dataset_fp = tf.keras.utils.get_file(fname=os.path.basename(train_dataset_url),origin=train_dataset_url)

print("Local copy of the dataset file: {}".format(train_dataset_fp))
def parse_csv(line):
  example_defaults = [[0.], [0.], [0.], [0.], [0]]  # sets field types
  parsed_line = tf.decode_csv(line, example_defaults)
  # First 4 fields are features, combine into single tensor
  features = tf.reshape(parsed_line[:-1], shape=(4,))
  # Last field is the label
  label = tf.reshape(parsed_line[-1], shape=())
  return features, label

train_dataset = tf.data.TextLineDataset(train_dataset_fp)
train_dataset = train_dataset.skip(1)             # skip the first header row
train_dataset = train_dataset.map(parse_csv)      # parse each row
train_dataset = train_dataset.shuffle(buffer_size=1000)  # randomize
train_dataset = train_dataset.batch(32)

# View a single example entry from a batch
features, label = tfe.Iterator(train_dataset).next()
print("example features:", features[0])
print("example label:", label[0])


#adventures in ML tutorial
const = tf.constant(2.0, name = 'const')
#b = tf.Variable(2.0, name='b')
b = tf.placeholder(tf.float32, [None, 1], name='b')
c = tf.Variable(1.0, name='c')

d = tf.add(b,c, name='d')
e = tf.add(c, const, name = 'e')
a = tf.multiply(d, e, name = 'a')
# setup the variable initialisation
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    #a_out = sess.run(a)
    a_out = sess.run(a, feed_dict={b: np.arange(0, 10)[:, np.newaxis]})
    print ('Variable a is {}', format(a_out))

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
#The one_hot=True argument specifies that instead of the labels associated with each image being the digit itself i.e. “4”, it is a vector with “one hot” node and all the other nodes being zero i.e. [0, 0, 0, 0, 1, 0, 0, 0, 0, 0].  This lets us easily feed it into the output layer of our neural network.

