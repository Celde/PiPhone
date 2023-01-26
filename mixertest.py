
import pygame
# 'KEPULU USB AUDIO Analog Stereo'


#pygame.mixer.pre_init(devicename='USB-Audio - KEPULU USB AUDIO')
pygame.mixer.pre_init(devicename='KEPULU USB AUDIO Analog Stereo')
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
sound = pygame.mixer.Sound('/home/pi/AudioRecordings/2023-01-19-17-50-16converted.wav')
sound.play()
while pygame.mixer.get_busy():
	print('playing sound hopefully')
