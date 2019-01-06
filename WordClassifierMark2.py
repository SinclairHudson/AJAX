#This Code is based on the tflearn classifier for IMDB reviews
#On the popular IMDB dataset.
from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
import os
import form

height = 128 #128 frequency ranges measured
print("getting the max utterance length")
length = form.get_max_word_length() #dynamic input ooooohhhh
print("max utterance length is "+str(length))
classes = 18 #ajax knows 18 words
batch_size = 64


# Network building
net = tflearn.input_data([None, length, height])
net = tflearn.embedding(net, input_dim=10000, output_dim=128)
net = tflearn.lstm(net, 128, dropout=0.8, dynamic=True)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy')

testX, testY = form.get_word_batch(200, length)
# Training
model = tflearn.DNN(net, tensorboard_verbose=3)
os.system("tensorboard --logdir=tmp/tflearn_logs/") #start tensorboard
model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True,
          batch_size=batch_size)
model.save("WordModels/wordClass.model")
