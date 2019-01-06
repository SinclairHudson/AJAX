from __future__ import print_function
# We'll need numpy for some mathematical operations
import numpy as np
from form import bladesmith
import librosa
import os
import shutil
start = 1
for i in range(51):
    audio_path = 'Sentences/sentence'+str(i+start)+'.wav'
    y, sr = librosa.load(audio_path,sr=20000,mono=True)
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(S, ref=np.max)
    print(log_S.shape)
    true = True
    slicybois = []
    print(audio_path)
    while true:
        inp=input("Type the break # or end to finish: ")
        if(inp=="end"):
            true = False #for the meme
        elif(inp=="play"):
            os.system("mplayer /media/sinclair/SINCLESTORE/JUNO/"+audio_path)
        elif(inp.isnumeric()):
            slicybois.append(int(inp))
        else:
            print("not valid, try again!")
        print(slicybois)
            
    name=""
    for i in range(len(slicybois)):
        name = name+str(slicybois[i])+"-"
    name = name+".wav"
    shutil.copy2('/media/sinclair/SINCLESTORE/JUNO/'+audio_path,
                 '/media/sinclair/SINCLESTORE/JUNO/MixedBreak/'+name)
    os.rename(audio_path, 'Sentences/0sentence'+str(i+start)+'.wav')
    print("Saving as Mixedbreak/"+name)
        #[22, 106, 83, 67, 54, 40]
