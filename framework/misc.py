import pygame
import math
import lucia
import time
from .sound3d import *
from .speech import *
key_holds=[]

class key_hold(object):
	def __init__(self, _key_code, _delay, _repeat):
		self.status=False
		self.key_flag=0
		self.key_code=_key_code
		self.delay=_delay
		self.repeat=_repeat
		self.repeat_time=self.delay
		self.key_timer=lucia.utils.timer.Timer()

	def pressing(self):
		self.status=lucia.key_down(self.key_code)
		if self.status==False:
			self.repeat_time=0
			self.key_timer.restart()
			self.key_flag=0
			return False
		if self.key_timer.elapsed>=self.repeat_time:
			if self.key_flag==0:
				self.key_flag=1
				self.repeat_time=self.delay
				self.key_timer.restart()
			elif self.key_flag==1:
				self.repeat_time=self.repeat
				self.key_timer.restart()
			return True
		return False

def key_holding(key, delay=500, repeat=50):
	for i in key_holds:
		if i.key_code==key:
			return i.pressing()
	key_holds.append(key_hold(key, delay, repeat))
	for i in key_holds:
		if i.key_code==key:
			return i.pressing()


def dlg(text, callback=None):
	speak(text)
	while True:
		lucia.process_events()
		time.sleep(0.005)
		if callback: callback
		if lucia.key_pressed(pygame.K_UP) or lucia.key_pressed(pygame.K_DOWN) or lucia.key_pressed(pygame.K_LEFT) or lucia.key_pressed(pygame.K_RIGHT):
			speak(text)
		if lucia.key_pressed(pygame.K_RETURN) or lucia.key_pressed(pygame.K_ESCAPE):
			break

def dlg_play(audio, audiotype="sound3d",callback=None, fade=False, fadespeed=30,context=None):
	dlgaudio=None
	if type(audio)==str:
		if audiotype=="sound3d":
			dlgaudio=sound3d("direct",context)
			dlgaudio.load(audio)
	else: return 0
	dlgaudio.play()
	while dlgaudio.is_playing():
		lucia.process_events()
		time.sleep(0.001)
		if callback: callback
		if lucia.key_pressed(pygame.K_RETURN):
			if fade:
				fade_sound(dlgaudio, -50, fadespeed)
			dlgaudio.stop()
			break

def plural(num,option1,option2):
	if num==1:
		return option1
	else:
		return option2

def grt(milliseconds):
	milliseconds=math.floor(milliseconds)
	seconds=math.floor((milliseconds/1000)%60)
	minutes=math.floor(((milliseconds/(1000*60))%60))
	hours=math.floor(((milliseconds/(1000*60*60))%24))
	days=int(milliseconds/1000/60/60/24)
	days=math.floor(days)
	hours=math.floor(hours)
	minutes=math.floor(minutes)
	seconds=math.floor(seconds)
	this1=""
	if days>0:
		this1=str(int(days))+":"
	this2=""
	if hours>0:
		this2=str(int(hours))+" "+plural(hours,"hour","hours")+", "

	this3=""
	if minutes>0:
		this3=str(int(minutes))+" "+plural(minutes,"minute","minutes")+", "

	this4=str(int(seconds))+" "+plural(seconds,"second","seconds")

	return this1+this2+this3+this4