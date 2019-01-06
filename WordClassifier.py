import tflearn
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import form
# Train 1: Jan 1 2019 - Only Achieved 80% Accuracy (unnacceptable)
# Train 2: Jan 4 2019 -

learning_rate = 0.0001 # slow learning rate for better accuracy
training_iters = 30000  # change back to 30 000steps
batch_size = 64

height = 128 # 128 frequency ranges measured
print("getting the max utterance length")
length = 68 # form.get_max_word_length() # dynamic input ooooohhhh
print("max utterance length is "+str(length))
classes = 18 # ajax knows 18 words
i = 0

# Network building
print("building NN")
net = tflearn.input_data([None,length,height]) # batchsize x time x freq
net = tflearn.lstm(net, 128, dropout=0.5)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
model = tflearn.DNN(net, tensorboard_verbose=3)
model.load("WordModels/wordClass.model") #load the model to continue training
for x in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES): tf.add_to_collection(tf.GraphKeys.VARIABLES, x )
print("finished NN")
# This is the sample set. Every once and a while the model takes this test of the same 200
# words and sees how it does. This is a consitent performance metric.
test_batch_x, test_batch_y = form.get_word_batch(200, length)

while i < training_iters:
        i = i+1
        trainX, trainY = form.get_word_batch(batch_size, length)
        model.fit(trainX, trainY, n_epoch=100, validation_set=(test_batch_x, test_batch_y),
                  show_metric=True, batch_size=batch_size)
        model.save("WordModels/wordClass.model")
