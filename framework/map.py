type_1d=0
type_2d=1
type_3d=2
type_2d_platformer=3
class map(object):
	def __init__(self,**kwargs):
		self.tiles=[]
		self.tile=kwargs.get('tile','')
		self.type=kwargs.get('type','2d')
		if self.type==type_1d:
			self.maxx=kwargs.get("maxx",-1)
			if self.tile!="":
				self.platform(minx=0,maxx=self.maxx,tile=self.tile)
		if self.type==type_2d:
			self.maxx=kwargs.get("maxx",-1)
			self.maxy=kwargs.get("maxy",-1)
			if self.tile!="":
				self.platform(minx=0,maxx=self.maxx,miny=0,maxy=self.maxy,tile=self.tile)
		if self.type==type_2d_platformer:
			self.maxx=kwargs.get("maxx",-1)
			self.maxy=kwargs.get("maxy",-1)
			if self.tile!="":
				self.platform(minx=0,maxx=self.maxx,miny=0,maxy=0,tile=self.tile)
		if self.type==type_3d:
			self.maxx=kwargs.get("maxx",-1)
			self.maxy=kwargs.get("maxy",-1)
			self.maxz=kwargs.get("maxz",-1)
			if self.tile!="":
				self.platform(minx=0,maxx=self.maxx,miny=0,maxy=self.maxy,minz=0,maxz=self.maxz,tile=self.tile)

	def platform(self,**kwargs):
		if self.type==type_1d:
			minx=kwargs.get("minx",-1)
			maxx=kwargs.get("maxx",-1)
			self.tiles.append(map_tile(minx,maxx,0,0,0,0,kwargs.get("tile","")))
		if self.type==type_2d:
			minx=kwargs.get("minx",-1)
			maxx=kwargs.get("maxx",-1)
			miny=kwargs.get("miny",-1)
			maxy=kwargs.get("maxy",-1)
			self.tiles.append(map_tile(minx,maxx,miny,maxy,0,0,kwargs.get("tile","")))
		if self.type==type_3d:
			minx=kwargs.get("minx",-1)
			maxx=kwargs.get("maxx",-1)
			miny=kwargs.get("miny",-1)
			maxy=kwargs.get("maxy",-1)
			minz=kwargs.get("minz",-1)
			maxz=kwargs.get("maxz",-1)
			self.tiles.append(map_tile(minx,maxx,miny,maxy,minz,maxz,kwargs.get("tile","")))

	def get_tile_at(self,**kwargs):
		tile=""
		if self.type==type_1d:
			x=kwargs.get("x",0)
			y=0
			z=0
		if self.type==type_2d:
			x=kwargs.get("x",0)
			y=kwargs.get("y",0)
			z=0
		if self.type==type_3d:
			x=kwargs.get("x",0)
			y=kwargs.get("y",0)
			z=kwargs.get("z",0)
		for i in self.tiles:
			if i.here(x,y,z):
				tile=i.tile
		return tile

def clear(self):
	self.tiles=[]

class map_tile(object):
	def __init__(self,minx,maxx,miny,maxy,minz,maxz,tile):
		self.minx=minx
		self.maxx=maxx
		self.miny=miny
		self.maxy=maxy
		self.minz=minz
		self.maxz=maxz
		self.tile=tile

	def here(self,x,y,z):
		if x>=self.minx and x<=self.maxx and y>=self.miny and y<=self.maxy and z>=self.minz and z<=self.maxz:
			return True
		return False
