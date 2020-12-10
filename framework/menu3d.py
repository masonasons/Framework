import pygame
import lucia
import time
from .speech import *
from .sound3d import *
from .misc import *
menu_object=1
menu_index=2
class menu_item3d(object):
	def __init__(self,text,name,is_tts,enabled):
		self.text=text
		self.name=name
		self.is_tts=is_tts
		self.enabled=enabled

class menu3d(object):
	def __init__(self, **kwargs):
		self.pool=kwargs.get('pool', None)
		self.callback=kwargs.get('callback', None)
		self.music=kwargs.get('music','')
		self.music_volume=kwargs.get('music_volume',-20)
		self.fade_music=kwargs.get('fade_music',False)
		self.fade_time=kwargs.get('fade_time',25)
		self.up_and_down=kwargs.get('up_and_down',True)
		self.left_and_right=kwargs.get('left_and_right',False)
		self.pan_sounds=kwargs.get('pan_sounds',False)
		self.click_sound=kwargs.get('click_sound','')
		self.enter_sound=kwargs.get('enter_sound','')
		self.edge_sound=kwargs.get('edge_sound','')
		self.wrap_sound=kwargs.get('wrap_sound','')
		self.open_sound=kwargs.get('open_sound','')
		self.escape_sound=kwargs.get('escape_sound','')
		self.return_type=kwargs.get('return_type',menu_object)
		self.at_edge=False
		self.position=-1
		self.items=[]
		self.home_and_end=kwargs.get('home_and_end',True)
		self.wrap=kwargs.get('wrap',False)
		self.select_with_enter=kwargs.get('select_with_enter',True)
		self.select_with_space=kwargs.get('select_with_space',False)
		self.announce_position_info=kwargs.get('announce_position_info',False)
		if self.music!="":
			self.mus=sound3d("direct",self.pool.context)
			self.mus.load(self.music)
			self.mus.volume=self.music_volume

	def get_item(self,index):
		return self.items(index-1)

	def add_item_tts(self,text,name, enabled=True):
		self.items.append(menu_item3d(text,name,True,enabled))

	def run(self,intro=None,is_intro_tts=True,starting_position=-1):
		if self.music!="":
			self.mus.play_looped()
		self.at_edge=False
		self.play(self.open_sound)
		self.position=starting_position
		if intro:
			if is_intro_tts:
				if starting_position==-1:
					speak(intro,1)
				else:
					speak(intro+". "+self.return_speak_item(),1)
			else:
				s=sound3d("direct",self.pool.context)
				s.load(intro)
				s.play()

		while 1:
			lucia.process_events()
			time.sleep(0.005)
			if self.callback:
				self.callback(self)
			if key_holding(pygame.K_PAGEUP) and self.music!="":
				if self.mus.volume<0:
					self.mus.volume+=1
			if key_holding(pygame.K_PAGEDOWN) and self.music!="":
				if self.mus.volume>-30:
					self.mus.volume-=1
			if key_holding(pygame.K_UP) and self.up_and_down==True or key_holding(pygame.K_LEFT) and self.left_and_right==True:
				self.cycle(1)
			elif key_holding(pygame.K_DOWN) and self.up_and_down==True or key_holding(pygame.K_RIGHT) and self.left_and_right==True:
				self.cycle(2)
			elif self.home_and_end:
				if lucia.key_pressed(pygame.K_HOME):
					self.at_edge=False
					self.position=0
					self.speak_item()
				elif lucia.key_pressed(pygame.K_END):
					self.at_edge=False
					self.position=len(self.items)-1
					self.speak_item()

			if (lucia.key_pressed(pygame.K_RETURN) and self.select_with_enter or lucia.key_pressed(pygame.K_SPACE) and self.select_with_space) and self.position!=-1:
				self.play(self.enter_sound)
				if self.items[self.position].enabled==True:
					self.kill_music()
					if self.return_type==menu_object:
						return self.items[self.position]
					else:
						return (self.position+1)

			if lucia.key_pressed(pygame.K_ESCAPE):
				self.play(self.escape_sound)
				self.kill_music()
				return -1

	def play(self,snd):
		if snd!="":
			if self.pan_sounds==False:
				self.pool.play_stationary(snd,False)
#			else:
#				self.pool.play_stationary_extended(snd,False, 0, convert_to_pan(len(self.items),self.position,-100,100),0,100)

	def cycle(self, dir):
		self.at_edge=False
		if dir==1:
			if self.position==-1:
				self.position=len(self.items)-1
			else:
				self.position-=1
			if self.position<0:
				if self.wrap==True:
					self.play(self.wrap_sound)
					self.position=len(self.items)-1
				else:
					self.position+=1
					self.at_edge=True
					self.play(self.edge_sound)
		if dir==2:
			if self.position==-1:
				self.position=0
			else:
				self.position+=1
			if self.position>len(self.items)-1:
				if self.wrap==True:
					self.play(self.wrap_sound)
					self.position=0
				else:
					self.position-=1
					self.at_edge=True
					self.play(self.edge_sound)
		self.speak_item()

	def speak_item(self):
		if self.at_edge==False:
			self.play(self.click_sound)
			speak(self.return_speak_item(),1)

	def return_speak_item(self):
		speaktext=self.items[self.position].text
		if self.announce_position_info==True:
			speaktext+=". "+str(self.position+1)+" of "+str(len(self.items))
		return speaktext

	def kill_music(self):
		if self.music!="":
			if self.fade_music==True:
				self.mus.fade(-40, self.fade_time)
			self.mus.stop()

	def fade(self, end=-40, time=None):
		if time==None: time=self.fade_time
		if self.music!="":
			self.mus.fade(end, time)
			self.mus.stop()

def convert_to_pan(length, index,  range1,  range2):
	range=range2-range1
	percent=0
	if length-1>0 and index>0:
		percent=index/(length-1)
	else:
		percent=0
	value=range1+range*percent
	return value
