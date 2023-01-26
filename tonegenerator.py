#!/usr/bin/env python3
#import scipy
from scipy.io.wavfile import write
from numpy import linspace,sin,pi,int16

def note(freq, len, amp=1, rate=44100):
	t = linspace(0, len, len * rate)
	data = sin(2 * pi * freq * t) * amp
	return data.astype(int16) # two byte integers
	
# tone = note(440, 2, amp=10000)
	
tone1 = note(1477, 10, amp=10000)
tone2 = note(941, 10, amp=10000)
tone = tone1 + tone2

write('1477hz+941hz(#).wav', 44100, tone) # writing the sound to a file


