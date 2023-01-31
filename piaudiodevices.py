import pygame


'''
import sounddevice

devs = sounddevice.query_devices()
print(devs)

for dev in devs:
	print(dev['name'])
'''

'''
import pygame
import pygame._sdl2.audio as sdl2_audio

def get_devices(capture_devices: bool = False) -> tuple[str, ...]:
	init_by_me = not pygame.mixer.get_init()
	if init_by_me:
		pygame.mixer.init()
	devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
	if init_by_me:
		pygame.mixer.quit()
	print(devices)
	return devices
	
get_devices
'''

import pygame
import pygame._sdl2 as sdl2
pygame.mixer.init()

pygame.init()
playback_devices = 0  # zero to request playback devices, non-zero to request recording devices
#num = sdl2.get_num_audio_devices(is_capture)
nums = sdl2.get_audio_device_names(playback_devices)
#names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(nums)]
names = []
for i in range(len(nums)):
	names.append(str(sdl2.get_audio_device_names(playback_devices)))
#names = [str(sdl2.get_audio_device_names
print("\n".join(names))
#print("got this far")
pygame.quit()



'''
#pygame.mixer.pre_init(devicename='USB-Audio - KEPULU USB AUDIO')
pygame.mixer.pre_init(devicename='1')
pygame.mixer.init()
pygame.init()



sound = pygame.mixer.Sound('350hz+440hz(dialtone).wav')
sound.play()

while pygame.mixer.get_busy():
	print("sound being played")
	pygame.time.delay(100)
'''

