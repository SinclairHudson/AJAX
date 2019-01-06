import tflearn
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import form
saveDIR = "/media/sinclair/SINCLESTORE/JUNO"
learning_rate = 0.0001 #slow learning rate for better accuracy
training_iters = 30000  # steps
batch_size = 64

height = 128
length = None #length is undefined, not a classifier
i = 0

# Network building
net = tflearn.input_data([length,height]) #length by 128 frequency ranges
net = tflearn.lstm(net, 128*4, dropout=0.5)
net = tflearn.fully_connected(net, length, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
model = tflearn.DNN(net, tensorboard_verbose=0)

for x in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES): tf.add_to_collection(tf.GraphKeys.VARIABLES, x )
# Training
test_batch_x, test_batch_y = form.get_batch(100)
while i < training_iters:
        i = i+1
        trainX, trainY = form.get_batch(batch_size)
        model.fit(trainX, trainY, n_epoch=100, validation_set=(test_batch_x, test_batch_y),
                  show_metric=True, batch_size=batch_size)
        model.save("BreakModels/break.model")
