
import pygame
# 'KEPULU USB AUDIO Analog Stereo'


#pygame.mixer.pre_init(devicename='USB-Audio - KEPULU USB AUDIO')
#pygame.mixer.pre_init(devicename='KEPULU USB AUDIO Analog Stereo')
pygame.mixer.init()
#pygame.init()


'''
sound = pygame.mixer.Sound('350hz+440hz(dialtone).wav')
sound.play()

while pygame.mixer.get_busy():
	print("sound being played")
	pygame.time.delay(100)
'''

#sound = pygame.mixer.Sound('recorded.wav')
try:
	sound = pygame.mixer.Sound('/home/pi/OriginalPiPhoneMessages/toolong.wav')
except:
	print('file was likely too long and did not open')
	sound = pygame.mixer.Sound('/home/pi/OriginalPiPhoneMessages/perfectintro.wav')
sound.play()

while pygame.mixer.get_busy():
	sleep(0.1)
	#print('playing sound hopefully')
