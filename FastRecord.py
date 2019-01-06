import GoogleSheets
import pyaudio
import wave
import time
import keyboard
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1024
k = 388 #start of indexing. DON'T OVERWRITE FILES


while True: #main loop
    script = GoogleSheets.fetch_command()[0]
    print("====================================================")
    arrayscript = script.split(" ")
    print("Your script is: "+script)
    audio = pyaudio.PyAudio() #initialize pyaudio
    print("Ctrl-C to start recording, and to stop")
    wordcount = len(arrayscript)
    print(wordcount)
    try: #this pauses until you're ready to record
        while True:
            blah = 0 #useless
    except KeyboardInterrupt:
        pass
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    print("recording... Press Ctrl-C to stop recording. ")
    frames = [] #the whole scentence
    wordframes = [] #used for capturing individual words
    allWords= [None] * wordcount #establish an array with wordcount elements
    flags = [] #used for finding spaces
    x=0 #used for keeping track of which word we're currently recording
    while True:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
            wordframes.append(data)
        except KeyboardInterrupt:
            flags.append(len(frames))
            print(x)
            allWords[x]=(wordframes)
            wordframes = []
            x=x+1
            if(x==wordcount):
                break
     
    # stop Recording
    print("finished recording")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    fileName = str(k)
    i=0
    print("saving...")
    for i in range(len(arrayscript)):#for each word
        #save the word file
        wordFile = "Words/"+str(k)+arrayscript[i]+".wav"
        waveFile = wave.open(wordFile, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(allWords[i]))
        waveFile.close()
        
        #build the main sentence file with indexes
        fileName = fileName + arrayscript[i] + str(flags[i])

    #save the main sentence file
    sentenceFile = "Sentences/"+fileName+".wav"
    waveFile = wave.open(sentenceFile, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    print("Finished Saving recording sentence "+str(k))
    #increment
    k = k+1
