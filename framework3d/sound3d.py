from . import rotation
import time
import math
import random
import synthizer
synthizer.initialize()
#Function for degrees from synthizer manual

def deg2rad(angle):
	return (angle/180.0)*math.pi

def make_orientation(degrees):
	rad=deg2rad(degrees)
	return (math.sin(rad), math.cos(rad), 0, 0, 0, 1)

#Sound buffer class, for handling synthizer sound buffers.
class sound_buffer(object):
	def __init__(self,filename,buffer):
		self.filename=filename
		self.buffer=buffer

	def destroy(self):
		self.buffer.destroy()

#Sound buffer manager class, for passing already loaded sound buffers if they exist, else creating new ones.
class sound_buffer_manager(object):
	def __init__(self):
		self.buffers=[]

	def buffer(self,filename):
		for i in self.buffers:
			if i.filename==filename:
#Our sound is already loaded into a buffer, so return it.
				return i.buffer
#Our sound is not loaded, so load it, add the buffer to the buffers list and return it.
		tmp=synthizer.Buffer.from_stream("file", filename)
		self.buffers.append(sound_buffer(filename,tmp))
		return tmp

	def destroy(self,buffer):
#Not used anywhere yet, todo.
		buffer.destroy()
		self.buffers.remove(self)

gsbm=sound_buffer_manager()
#The actual sound3D class.
class sound3d(object):
	def __init__(self, type,context):
		self.context=context
		self.type=type
		self.vol=0
		self.handle=0
		self.paused=False
		self.filename=""
		self.buffer=None
		self.source=None
		self.generator=None
		self.length=None

	def load(self, filename):
		if self.handle!=None: self.close()
		if isinstance(filename, str): # Asume path on disk.
			self.generator=synthizer.BufferGenerator(self.context)
			self.buffer=gsbm.buffer(filename)
			self.length=self.buffer.get_length_in_seconds()
			self.generator.buffer=self.buffer
			if self.type=="3d":
				self.source = synthizer.Source3D(self.context)
			elif self.type=="direct":
				self.source = synthizer.DirectSource(self.context)
			elif self.type=="panned":
				self.source = synthizer.PannedSource(self.context)
		self.generator.pause()
		self.source.add_generator(self.generator)
		self.paused=True
		if self.is_active:
			self.filename=filename
			return True
		return False

	def close(self):
		if not self.is_active():
			return False
		self.source.remove_generator(self.generator)
		self.source.destroy()
		self.generator.destroy()
		self.source=None
		self.buffer=None
		self.generator=None
		self.filename=""

	def play(self):
		if not self.is_active():
			return False
		self.generator.looping=False
		self.generator.play()
		self.paused=False
		self.looping=False
		return True

	def play_looped(self):
		if not self.is_active():
			return False
		self.generator.looping=True
		self.generator.play()
		self.paused=False
		self.looping=True
		return True

	def play_wait(self):
		if not self.is_active():
			return False
		self.generator.looping=False
		self.play()
		while self.is_playing():
			time.sleep(0.005)
		return True

	def is_playing(self):
		return self.position<=self.length-0.005

	def pause(self):
		if not self.is_active():
			return False
		self.generator.pause()
		self.paused=True

	def stop(self):
		if not self.is_active():
			return False
		self.generator.pause()
		self.generator.position=0
		self.paused=False

	def get_position(self):
		if not self.is_active():
			return -1
		return self.generator.position

	def set_position(self, position):
		if not self.is_active():
			return False
		self.generator.position=position
		return True

	def get_volume(self):
		if not self.is_active():
			return 0
		return self.vol

	def set_volume(self, volume):
		if not self.is_active():
			return False
		if volume>0: volume=0
		self.vol=volume
#using formula from the example code to convert to DB
		self.source.gain=10**(volume/20)

	def get_pitch(self):
		if not self.is_active():
			return 100
		return self.generator.pitch_bend*100

	def set_pitch(self, pitch):
		if not self.is_active():
			return False
		freq=(float(pitch)/100)
		if freq>10: freq=10
		if freq<0.1: freq=0.1
		self.generator.pitch_bend=freq

	def get_pan(self):
		if not self.is_active():
			return 0
		if self.type=="panned":
			return int(self.source.panning_scaler*100)
		else:
			return 0

	def set_pan(self, pan):
		if not self.is_active():
			return False
		if self.type!="panned":
			return False
		self.source.panning_scalar=pan/100

	def is_active(self):
		if self.source!=None:
			try:
				pb=self.generator.position
			except: return False
			return True
		return False

	pan=property(get_pan, set_pan)
	pitch=property(get_pitch, set_pitch)
	volume=property(get_volume, set_volume)
	position=property(get_position, set_position)
	active=property(is_active)

#Fade a sound.
	def fade(self,dest_volume, time_per_fade):
		while self.volume!=dest_volume:
			if self.volume<dest_volume: self.volume=self.volume+1
			if self.volume>dest_volume: self.volume=self.volume-1
			time.sleep(time_per_fade/1000)
		self.stop()
		return True

#Sound manager. This is a sound pool, of sorts. Very rough. We support reverb only so far.
class sound_manager_item(object):
	def __init__(self,filename,looping,type="",context=None,x=0,y=0,z=0,verb=True):
		self.filename=filename
		self.verb=verb
		self.looping=looping
		self.delete=False
		self.x=x
		self.y=y
		self.z=z
		self.handle=sound3d(type,context)
		try:
			result=self.handle.load(filename)
		except:
			self.delete=True
			return
		if type=="3d":
			self.handle.source.position=(self.x,self.y,self.z)

	def destroy(self):
		self.handle.close()

class sound_manager(object):
	def __init__(self):
		self.sounds=[]
		self.ex=0
		self.ey=0
		self.ez=0
		self.context=synthizer.Context()
		self.max_distance=100
		self.internal_reverb = synthizer.GlobalFdnReverb(self.context)
		self.verb=False
		self.orientation=0
		self.facing=0
		self.is_cleaning=False

	def set_facing(self,facing):
		self.context.orientation=make_orientation(facing)
		self.orientation=facing

	def get_facing(self):
		return self.orientation

	facing=property(get_facing,set_facing)

	def set_distance(self,distance):
		self.context.distance_max=distance
		self.max_distance=distance

	def get_distance(self):
		return self.max_distance

	distance=property(get_distance,set_distance)

	def set_hrtf(self,hrtf):
		if hrtf==False:
			self.context.panner_strategy=self.context.panner_strategy.STEREO
		else:
			self.context.panner_strategy=self.context.panner_strategy.HRTF

	def get_hrtf(self):
		if self.context.panner_strategy==self.context.panner_strategy.STEREO:
			return False
		else:
			return True

	hrtf=property(get_hrtf,set_hrtf)

	def set_x(self,x):
		self.ex=x
		self.context.position=(self.x,self.y,self.z)
		self.update_sounds()

	def get_x(self):
		return self.ex
	x=property(get_x,set_x)

	def set_y(self,y):
		self.ey=y
		self.context.position=(self.x,self.y,self.z)
		self.update_sounds()

	def get_y(self):
		return self.ey
	y=property(get_y,set_y)

	def set_z(self,z):
		self.ez=z
		self.context.position=(self.x,self.y,self.z)
		self.update_sounds()

	def get_z(self):
		return self.ez
	z=property(get_z,set_z)

	def get_verb(self):
		return self.verb

	def set_verb(self,verb):
		self.verb=verb
		for i in self.sounds:
			if verb==True and i.verb==True:
				self.context.config_route(i.handle.source, self.internal_reverb)
			else:
				self.context.remove_route(i.handle.source, self.internal_reverb)

	reverb=property(get_verb,set_verb)

	def get_id(self):
		id=random.randint(100000000, 999999999)
		tries=0
		while self.get_item(id)!=0 and tries<500:
			id=random.randint(100000000, 999999999)
			tries+=1
		if tries>=500: return -1
		return id

	def get_item(self, id):
		for i in self.sounds:
			if id==i.id: return i
		return 0

	def destroy_sound(self, id):
		i=self.get_item(id)
		if i==0: return False
		i.destroy()
		self.sounds.remove(i)

	def play_stationary(self,filename,looping=False,verb=True):
		self.clean()
		i=sound_manager_item(filename,looping,"direct",self.context,0,0,0,verb)
		if i.delete==True:
			del i
			return False
		if self.reverb==True and i.verb==True:
			self.context.config_route(i.handle.source, self.internal_reverb)
		i.id=self.get_id()
		if looping==False:
			i.handle.play()
		else:
			i.handle.play_looped()
		self.sounds.append(i)
		return i.id

	def play_1d(self,filename,x,looping=False,verb=True):
		return self.play_3d(filename,x,0,0,looping,verb)

	def play_2d(self,filename,x,y,looping=False,verb=True):
		return self.play_3d(filename,x,y,0,looping,verb)

	def play_3d(self,filename,x,y,z,looping=False,verb=False):
		self.clean()
		i=sound_manager_item(filename,looping,"3d",self.context,x,y,z,verb)
		if i.delete==True:
			del i
			return False
		if self.reverb==True and i.verb==True:
			self.context.config_route(i.handle.source, self.internal_reverb)
		i.id=self.get_id()
		if rotation.get_3d_distance(self.x,self.y,self.z,i.x,i.y,i.z)<=self.distance:
			if looping==False:
				i.handle.play()
			else:
				i.handle.play_looped()
		self.sounds.append(i)
		return i.id

	def update_1d(self,id,x):
		return self.update_3d(id,x,0,0)

	def update_2d(self,id,x,y):
		return self.update_3d(id,x,y,0)

	def update_3d(self,id,x,y,z):
		self.clean()
		i=self.get_item(id)
		if i==0:
			return False
		if i.handle.type!="3d":
			return False
		i.handle.source.position=(x,y,z)
		if rotation.get_3d_distance(self.x,self.y,self.z,i.x,i.y,i.z)<=self.distance and i.handle.is_playing()==False:
			if i.looping==False:
				i.handle.play()
			else:
				i.handle.play_looped()
		return True

	def update_pan(self,id,pan):
		self.clean()
		i=self.get_item(id)
		if i==0:
			return False
		if i.handle.type!="panned":
			return False
		i.handle.pan=pan
		return True

	def update_pitch(self,id,pitch):
		i=self.get_item(id)
		if i==0:
			return False
		i.handle.pitch=pitch
		return True

	def update_volume(self,id,volume):
		i=self.get_item(id)
		if i==0:
			return False
		i.handle.volume=volume
		return True

	def update_sounds(self):
		for i in self.sounds:
			if i.handle.type=="3d":
				if rotation.get_3d_distance(self.x,self.y,self.z,i.x,i.y,i.z)<=self.distance and i.handle.is_playing()==False:
					if i.looping==False:
						i.handle.play()
					else:
						i.handle.play_looped()
				elif rotation.get_3d_distance(i.x,i.y,i.z,self.x,self.y,self.z)>self.distance and i.handle.is_playing()==True:
					i.handle.pause()

	def clean(self):
		sounds_to_clean=[]
		for i in self.sounds:
			if i.looping: continue
			if not i.handle.is_playing() and not i.handle.paused:
				sounds_to_clean.append(i)
		for i in sounds_to_clean:
			i.destroy()
			self.sounds.remove(i)

	def destroy_all(self):
		for i in self.sounds:
			i.handle.stop()
			i.destroy()
		self.sounds=[]

	def destroy_sound(self,id):
		i=self.get_item(id)
		if i==0:
			return False
		i.handle.stop()
		time.sleep(0.005)
		i.destroy()
		self.sounds.remove(i)
		return True

	def playing(self,id):
		i=self.get_item(id)
		if i==0:
			return False
		return i.handle.is_playing()