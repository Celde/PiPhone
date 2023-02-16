#!/usr/bin/env python3

#testing audio recording with python

import pyaudio
import wave
from datetime import datetime

# the file name output you want to record into
#filename = "recorded.wav"
#/home/pi/AudioRecordings
#now.datetime()%Y-%m-%d-%H-%M-%S

now = datetime.now()
currenttime = now.strftime("%m-%d-%Y %H:%M:%S")
filename = '/home/pi/AudioRecordings/{}.wav'.format(currenttime)

#set the chunk size of 1024 samples
chunk = 1024

# sample format
FORMAT = pyaudio.paInt16

# mono, change to 2 if you want stereo
channels = 1

# 44100 samples per second
#sample_rate = 44100
sample_rate = 48000 # this was the default for the device after digging into it, and it didnt' seem to like 44100


record_seconds = 5



# initialize PyAudio object
p = pyaudio.PyAudio()

# trying to select recording device, only accepts integer
# uspecified uses default
#devicename='KEPULU USB AUDIO Analog Stereo' - this was for pygame
#0 - appears to be bcmheadphones, which I believe is default
#1 - same
# Input Device id  1  -  KEPULU USB AUDIO: Audio (hw:1,0) generated
#from indexing the pyaudio device list. So 1 should be accurate



# open stream object as input and output
stream = p.open(format=FORMAT,
input_device_index=1,
channels=channels,
rate=sample_rate,
input=True,
output=True,
frames_per_buffer=chunk)


frames = []
print('Recording...')

for i in range(int(sample_rate / chunk * record_seconds)):
	data = stream.read(chunk)
	# if you want to hear your voice while recording
	# stream.write(data)
	frames.append(data)



print("finished recording.")

stream.stop_stream()
stream.close()
# terminate pyaudio object
p.terminate()
#save audio file
# open the file in 'write bytes' mode
wf = wave.open(filename, "wb")

#set the chnnels
wf.setnchannels(channels)

# set the sample format
wf.setsampwidth(p.get_sample_size(FORMAT))

# set the sample rate
#wf.wetframerate(sample_rate)
wf.setframerate(sample_rate)

# write the frames as bytes
wf.writeframes(b"".join(frames))

# close the file
wf.close()
