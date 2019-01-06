import tflearn
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import librosa
import os
import random

Dictionary=[ #All the words that Ajax knows
"ajax",
"please",
"email",
"open",
"messenger",
"gmail",
"radar",
"get",
"do",
"weather",
"like",
"today",
"what",
"looking",
"is",
"the",
"pull",
"up"]

wordfilelist = os.listdir("/media/sinclair/SINCLESTORE/JUNO/Words")
#this function returns a testing/training batch, which is really just
#a stack of audio forms and a stack of matching labels
#length is a param here because it's not efficient to call
#get_max_word_length more than once
def get_word_batch(batch_size, length):
    #these are basis inputs that are added to. They
    #are here so that I have something to stack on top of.
    x = np.array([pad(get_audio_array("Words/0ajax.wav"), length)])
    y = np.array([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    for i in range(batch_size-1): #for batchsize number of times
        #choose a random file
        index = random.randint(0,len(wordfilelist)-1)
        filename = wordfilelist[index]
        #add it's audio data to the stack, and add its label
        #to the stack
        z = np.array([pad(get_audio_array("Words/"+filename), length)])
        x = np.append(x, z, axis=0)
        a = np.array([get_label_from_word_file_name(filename)])
        y = np.append(y, a, axis=0)
    x = np.swapaxes(x, 1, 2)
    return x, y #return the two stacks                              

def get_audio_array(path): #get the audio data from a file
    y, sr = librosa.load(path,sr=20000,mono=True)
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    return log_S

#pads the audio signal at the end with -1s, until it's the desired
#length
def pad(audio_array, length):
    if(audio_array.shape[1]==length): #no padding required
        return audio_array
    else:
        padding = np.full((128, length - audio_array.shape[1]), -1)
        return np.append(audio_array, padding, axis=1)
    
    
    
def get_label_from_word_file_name(filename):
    label=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #blank label
    #taking out the number in front from the filename
    betterfile = ''.join(i for i in filename if not i.isdigit())
    word = betterfile.split(".")[0] #removing the .wav
    for x in range(len(Dictionary)):
        if Dictionary[x] == word:
            label[x]=1
            break
    return label

#this algorithm requires padding, because the audio utterances
#are of different length. So we need to find the max length of all
#audio utterances so that we know just how much to pad. This will
#keep the data to a minimum and reduce training time.
#this function looks at all the words in the dataset and finds the
#longest one, and outputs that. (it takes a while to run)
def get_max_word_length():
    maxim = 0
    for x in range(len(wordfilelist)-1):
        audio=get_audio_array("Words/"+wordfilelist[x])
        if (maxim < audio.shape[1]):
            maxim = audio.shape[1]
    return maxim
        
def bladesmith(numbers,length):
    blade = np.zeros(length)
    for x in range(length):
        if x in numbers:
            blade[x]=1
    return blade

def slicer(blade, bread):
    slicelines = []
    for x in range(len(blade)):
        if blade[x] == 1: # if the blade makes and appearance
            slicelines.append(x)#add it to the list of cut lines
    return np.split(bread,slicelines) #return sliced bread
