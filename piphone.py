#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from pygame import mixer
from datetime import datetime
import random
import os
import pyaudio
import wave
# import piphonerecord


#Col0Pin = 21  # setting the pins to meaningful variables
Col0Pin = 12
Col1Pin = 20
Col2Pin = 16

Row0Pin = 26
#Row1Pin = 19
Row1Pin = 5
Row2Pin = 13
Row3Pin = 6

#Btnpin = 18
Btnpin = 24


'''delcare variables'''
#off_cradle = 0
on_cradle = 1  # status of phone on cradle
first_hang = 1  # varable used so dialtone doesn't resume after buttons are pushed
keypad_status = 0  # keypad status, off when phone on cradle
#global typednumber
typednumber = ''
#global typednumber


#set the chunk size of 1024 samples
chunk = 1024

# sample format
FORMAT = pyaudio.paInt16

# mono, change to 2 if you want stereo
channels = 1

# 44100 samples per second
#sample_rate = 44100
sample_rate = 48000 # this was the default for the device after digging into it, and it didnt' seem to like 44100





'''initializing pygame sound mixer'''
#mixer.pre_init(devicename='KEPULU USB AUDIO Analog Stereo')
# omitting pre_init uses default which fortunately is the hifi DAC
mixer.init()


''' creating sound objects '''
# keep in mind, pygame mixer can only play uncompressed wav and ogg files

welcomemessage = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/thankyou.wav')
dialtone = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/350hz+440hz(dialtone).wav')
dial1 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1209hz+697hz(#1).wav')
dial2 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1336hz+697hz(#2).wav')
dial3 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1477hz+697hz(#3).wav')
dial4 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1209hz+770hz(#4).wav')
dial5 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1336hz+770hz(#5).wav')
dial6 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1477hz+770hz(#6).wav')
dial7 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1209hz+852hz(#7).wav')
dial8 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1336hz+852hz(#8).wav')
dial9 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1477hz+852hz(#9).wav')
dial0 = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1336hz+941hz(#0).wav')
dialstar = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1209hz+941hz(*).wav')
diallb = mixer.Sound('/home/pi/PiPhone/PiPhoneAudioFiles/1477hz+941hz(#).wav')


def setup(): #  initial set up of pins and parameters
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
	GPIO.setwarnings(False)
	
	GPIO.setup(Col0Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #  Pin is 'off' until contact is made
	GPIO.setup(Col1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(Col2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	GPIO.add_event_detect(Col0Pin, GPIO.BOTH, callback=columncheck, bouncetime=100)  # Adding event detection on column channels
	GPIO.add_event_detect(Col1Pin, GPIO.BOTH, callback=columncheck, bouncetime=100)
	GPIO.add_event_detect(Col2Pin, GPIO.BOTH, callback=columncheck, bouncetime=100)
	
	GPIO.setup(Row0Pin, GPIO.OUT)
	GPIO.output(Row0Pin, GPIO.HIGH) #  Setting row 0 to high output
	GPIO.setup(Row1Pin, GPIO.OUT)
	GPIO.output(Row1Pin, GPIO.HIGH)
	GPIO.setup(Row2Pin, GPIO.OUT)
	GPIO.output(Row2Pin, GPIO.HIGH)
	GPIO.setup(Row3Pin, GPIO.OUT)
	GPIO.output(Row3Pin, GPIO.HIGH)
	
	GPIO.setup(Btnpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull up, should be it starts on, when button is activated, it turns off.



def restartsetup(): #  Called function that returns pins to a state ready for another keypress
	GPIO.setup(Col0Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(Col1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(Col2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	GPIO.setup(Row0Pin, GPIO.OUT)
	GPIO.output(Row0Pin, GPIO.HIGH) #  Setting row 0 to high output
	GPIO.setup(Row1Pin, GPIO.OUT)
	GPIO.output(Row1Pin, GPIO.HIGH)
	GPIO.setup(Row2Pin, GPIO.OUT)
	GPIO.output(Row2Pin, GPIO.HIGH)
	GPIO.setup(Row3Pin, GPIO.OUT)
	GPIO.output(Row3Pin, GPIO.HIGH)
	
	mixer.stop()

'''
def disable_keypad():
	GPIO.output(Row0Pin, GPIO.LOW)  # disabling keypad by turning rows to no output
	GPIO.output(Row1Pin, GPIO.LOW)
	GPIO.output(Row2Pin, GPIO.LOW)
	GPIO.output(Row3Pin, GPIO.LOW)
	keypad_status = 0  # keypad_status set to 0 for 'off'
	
def enable_keypad():
	GPIO.output(Row0Pin, GPIO.HIGH)  # enabling keypad by turning rows to high output
	GPIO.output(Row1Pin, GPIO.HIGH)
	GPIO.output(Row2Pin, GPIO.HIGH)
	GPIO.output(Row3Pin, GPIO.HIGH)
	keypad_status = 1  # keypad_status set to 1 for 'on'
'''
	


def testcall(): #  func to evaluate pin states
	print("Pin Values")
	print("Column1", GPIO.input(Col0Pin))
	print("Column2", GPIO.input(Col1Pin))
	print("Column3", GPIO.input(Col2Pin))
	print("Row1", GPIO.input(Row0Pin))
	print("Row2", GPIO.input(Row1Pin))			
	print("Row3", GPIO.input(Row2Pin))
	print("Row4", GPIO.input(Row3Pin))
	print("cradle status", GPIO.input(Btnpin))
	

def columncheck(channel):
	mixer.stop()
	if GPIO.input(channel) == 1: #  0 is off, 1 is on
		GPIO.setup(channel, GPIO.OUT)  # if column is activated, it becomes a source of output
		GPIO.output(channel, GPIO.HIGH)
		rowcheck(channel)  # evaluates rows to determine which button is being pressed
	restartsetup()  # this will reset columns to wait for input

def rowcheck(channel):
	GPIO.setup(Row0Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(Row1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(Row2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(Row3Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	global typednumber
	
	if channel == Col0Pin:
		if GPIO.input(Row0Pin) == 1:
			print("1")
			if keypad_status:
				typednumber += '1'
				dial1.play()
			GPIO.wait_for_edge(Row0Pin, GPIO.FALLING)
		if GPIO.input(Row1Pin) == 1:
			print("4")
			if keypad_status:
				typednumber += '4'
				dial4.play()
			GPIO.wait_for_edge(Row1Pin, GPIO.FALLING)
		if GPIO.input(Row2Pin) == 1:
			print("7")
			if keypad_status:
				typednumber += '7'
				dial7.play()
			GPIO.wait_for_edge(Row2Pin, GPIO.FALLING)
		if GPIO.input(Row3Pin) == 1:
			print("*")
			if keypad_status:
				typednumber += '*'
				dialstar.play()
			GPIO.wait_for_edge(Row3Pin, GPIO.FALLING)
			
	if channel == Col1Pin:
		if GPIO.input(Row0Pin) == 1:
			print("2")
			if keypad_status:
				dial2.play()
				typednumber += '2'
			GPIO.wait_for_edge(Row0Pin, GPIO.FALLING)
		if GPIO.input(Row1Pin) == 1:
			print("5")
			if keypad_status:
				dial5.play()
				typednumber += '5'
			GPIO.wait_for_edge(Row1Pin, GPIO.FALLING)
		if GPIO.input(Row2Pin) == 1:
			print("8")
			if keypad_status:
				dial8.play()
				typednumber += '8'
			GPIO.wait_for_edge(Row2Pin, GPIO.FALLING)
		if GPIO.input(Row3Pin) == 1:
			print("0")
			if keypad_status:
				dial0.play()
				typednumber += '0'
			GPIO.wait_for_edge(Row3Pin, GPIO.FALLING)
			
	if channel == Col2Pin:
		if GPIO.input(Row0Pin) == 1:
			print("3")
			if keypad_status:
				dial3.play()
				typednumber += '3'
			GPIO.wait_for_edge(Row0Pin, GPIO.FALLING)
		if GPIO.input(Row1Pin) == 1:
			print("6")
			if keypad_status:
				dial6.play()
				typednumber += '6'
			GPIO.wait_for_edge(Row1Pin, GPIO.FALLING)
		if GPIO.input(Row2Pin) == 1:
			print("9")
			if keypad_status:
				dial9.play()
				typednumber += '9'
			GPIO.wait_for_edge(Row2Pin, GPIO.FALLING)
		if GPIO.input(Row3Pin) == 1:  # '#' will interrupt everything except cradle status, play welcome message and then begin recording
			print("#")
#			print(typednumber)
			if keypad_status:
				typednumber = ''
				welcomemessage.play()
				time.sleep(welcomemessage.get_length())
				record_and_save()
#			GPIO.wait_for_edge(Row3Pin, GPIO.FALLING)
#			os.system("aplay -D plughw:CARD=AUDIO,DEV=0 thankyou.wav")
#			print("message has completed, recording has begun")
#			now = datetime.now()
#			os.system("arecord -D plughw:CARD=AUDIO,DEV=0 --use-strftime %Y-%m-%d-%H-%M-%S.wav")
#			print("message recorded")



def evaluate_typed_number():
	global typednumber
	if typednumber == '263':
		typednumber = ''
		print('TYPED NUMBER 263')
		randfiles = []
		files = os.listdir('/home/pi/PiPhoneAudioMessages')
		randfiles = [i for i in files]
		print(randfiles)
		ri = random.randint(0, len(randfiles) - 1)  # random index
		randomvoicemail = mixer.Sound('/home/pi/PiPhoneAudioMessages/' + files[ri])
		randomvoicemail.play()


def record_and_save():
	now = datetime.now()
	currenttime = now.strftime("%m-%d-%Y %H:%M:%S")
	filename = '/home/pi/PiPhoneAudioMessages/{}.wav'.format(currenttime)
	
	# initialize PyAudio object
	p = pyaudio.PyAudio()
	# open stream object as input and output
	stream = p.open(format=FORMAT,
	input_device_index=1,
	channels=channels,
	rate=sample_rate,
	input=True,
#	output=True,  # output should reflect pyaudio output to speakers
	frames_per_buffer=chunk)
	frames = []
	
	print('Recording...')
	
	while not on_cradle:
		data = stream.read(chunk)
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



def mainloop():
	if not mixer.get_busy():
		global first_hang
		if first_hang:
			dialtone.play()
	first_hang = 0
#	print('dialtone should be playing')
	time.sleep(0.3)
	evaluate_typed_number()
	
'''
	print('mainloop')
	if off_cradle == True:
		time.sleep(0.1)
		print('off cradle')
		if not mixer.get_busy:
			dialtone.play()
	else:
		restartsetup()
	'''	
		
		



def destroy():
	GPIO.cleanup()

	
if __name__ == '__main__':     # Program start from here
	setup()
	testcall()
	try:
		while True:
			on_cradle = GPIO.input(Btnpin)
#			print(GPIO.input(Btnpin))
			if on_cradle:
#				on_cradle_resets()
#				print('keypadstatus=',keypad_status)
				keypad_status = 0
				first_hang = 1
				typednumber = ''
				mixer.stop()

				
			time.sleep(0.1)
			#print('can i get here?')
			if not on_cradle:
				keypad_status = 1
				mainloop()
			
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

