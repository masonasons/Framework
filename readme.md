Welcome to Framework.

# What is Framework?

Framework is the python 3 compatible audiogame creation toolkit. It combines many things and aims to make it simple to create audiogames in Python.

Note! Some things are still undocumented!

# Requirements
* pygame
* synthizer (pip install synthizer)
* cytolk (pip install cytolk)

# Credits
This toolkit has been Created by Mason Armstrong. BGT style Sound class and sound manager created initially for Sound_Lib by Carter Temm and continued/adapted to Synthizer by Mason Armstrong. Initial sound_pool class for sound_lib created by Kianoosh and updated/finished by Mason Armstrong. Menu and map classes created by Mason Armstrong. Some code originally part of the AGK and AGK3 packages.

# What do we have?

## Classes

### sound3d
sound class for manually manipulating sounds.
### constructor
sound3d(type, context)
type (string): direct, pannable, or 3D. Check the synthizer documentation on what each one of these does.
context: A synthizer context object.
#### Functions
sound.load("filename.extension")
Load a sound into memory.
sound.close()
close a sound from memory.
sound.play()
play a sound once.
sound.play_looped()
play a sound looped.
sound.play_wait()
play a sound and wait until it is finished.
sound.pause()
pause a sound.
sound.stop()
stop a sound

Sound Properties
active: Read only Boolean which tells if a sound is active or not.
paused: Read only Boolean which tells if a sound is paused or not.
pan: A number between -100 and 100 which specifies the pan of a sound. This only works for pannable sounds.
pitch: A number between 0 and infinity which sets the pitch of a sound. 100 is normal, above is higher and below is lower.
volume: A number which sets the volume (in DB) of a sound. 0 is loudest, below is quieter.
position: A number which sets and shows the seek position (in ms) of a sound.
length: A read only number showing the length of a sound in seconds.
playing: gets the status of a sound, playing is True.

## sound_manager
a high level class for handling sounds.
### Functions:
sound_manager.play_stationary(filename,looping)
Play a sound in the center, either one shot or looped. Returns the sound object for later manipulation.
sound_manager.play_1d(filename, sound_x, looping)
Play a sound in a 1 Dementional setting. Returns the object for later manipulation.
sound_manager.play_2d(filename, sound_x, sound_y, looping)
Play a sound in a 2 Dementional setting. Returns the object for later manipulation.
sound_manager.play_3d(filename, sound_x, sound_y, sound_z, looping)
Play a sound in a 3 Dementional setting. Returns the object for later manipulation.

sound_manager.destroy_all()
destroy all playing sounds.
### properties
sound_manager.facing
The player's facing direction (Orientation), in degrees.
sound_manager.distance
the maximum distance from which sounds will be heard
sound_manager.hrtf
True or False for HRTF positioning. If false, stereo is used.
sound_manager.x, sound_manager.y and sound_manager.z.
Update a listener's position.


### SoundManager item properties
x, y, and z: set the position of the sound.
pitch, volume
set the pitch and volume of the sound
playing, active
read only properties querying the status of the sound.

### Sound manager item methods
update(x,y,z)
update the position of the sound. This is an alternative for setting x, y and Z.

## Menu
A class for creating and displaying a menu.
### menu(arguments)
All arguments are optional. Valid arguments:
music=""
set music to play in this menu.
music_volume=-20
set the initial music volume.
fade_music=False
Set if the music will fade by default or not.
fade_time=25
Set how fast the music fades.
up_and_down=True
enable the up and down arrows.
left_and_right=False
Set if left and right arrows work in the menu.
pan_sounds=False
set if menu sounds pan relative to the position you are in the menu. Doesn't work since converting to synthizer yet.
click_sound=""
set a click sound for your menu.
enter_sound=""
set a sound for when you press enter on the item.
edge_sound=""
set a sound for your menu hitting the edge.
wrap_sound=""
set a sound for a wrapping menu.
open_sound=""
set a sound for a menu opening.
escape_sound=""
set a sound for escaping out of the menu.
return_type=menu_object
set the return type, either menu_index or menu_object. If index, when you run the run option, you will be returned a menu_item which has the values text and name.
home_and_end=True
set if the menu allows home and end.
wrap=False
set if the menu wraps
select_with_enter=True
select if enter selects menu items.
select_with_space=False
select if space selects menu items.
announce_position_info=False
select if position info is announced, such as 1 of 4.

### Functions
get_item(index)
get a menu item object from an index.
add_item_tts(text_to_speak,name_of_item,item_enabled=True)
add a tts item to the menu. Disabling the item will disallow enter press on the item.
run(intro=None,tts_intro=True,starting_position=-1)
run the menu! Returned item is shown above.


## Map
This class allows you to create 1D, 2D, or 3D maps and query tiles at positions. It is new, so therefore may be missing crucial features.
### your_map=map(type)
This function accepts different perametors based on what type you select. The choices are:
type_1d
type_2d
type_3d
if you choose type=type_1d, the other perametors are:
maxx
the maximum x of this map.
tile
the default surface of this map.
if you choose type=type_2d, the other perametors are:
maxx
the maximum x of this map.
maxy
the maximum y of this map.
tile
the default surface of this map.
if you choose type=type_2d_platformer, the other perametors are:
maxx
the maximum x of this map.
maxy
the maximum y of this map.
tile
the default surface of this map.
The difference is that tiles will only be spawned the maximum x at y 0, and not all Y's.
if you choose type=type_3d, the other perametors are:
maxx
the maximum x of this map.
maxy
the maximum y of this map.
maxz
the maximum z of this map.
tile
the default surface of this map.
Example for spawning a 2D map
my_map=map(type=type_2d,tile="concrete",maxx=40,maxy=20)

### Functions
platform(arguments)
if 1d, arguments are:
minx=number, maxx=number, tile=""
if 2d, arguments are:
minx=number, maxx=number, miny=number, maxy=number, tile=""
if 3d, arguments are:
minx=number, maxx=number, miny=number, maxy=number, minz=number, maxz=number, tile=""
example
my_map.platform(minx=0,maxx=15,miny=0,maxy=4,minz=0,maxz=0,tile="rocks")

map.get_tile_at(arguments)
if 1d, arguments are
x
if 2d, arguments are
x, y
if 3d, arguments are
x, y, z
Example
tile=my_map.get_tile_at(x=5,y=3,z=0)


## Window

Taken from Lucia and adapted for Framework.

###Functions

window.initialize()
You must call this function at the top of your code. It initializes pygame.

quit()
Frees pygame.

show_window(title,size)
Shows a window on the screen. Title and size are optional.

process_events()
You must call this in your main loop, otherwise the window will become not responding.

key_pressed(key)
check if a key is pressed or not. E.G. window.key_pressed(window.K_left)

key_released(key)
check if a key is released or not. E.G. window.key_released(window.K_left)

key_down(key)
check if a key is being held down or not. E.G. window.key_down(window.K_left)

key_up(key)
check if a key is not being held down. E.G. window.key_up(window.K_left)

## timer
Timer class, taken from lucia and adapted for Framework.

### Functions
timer.restart()
Restarts the timer back to 0 MS

timer.pause()
pause a timer.

timer.resume()
resume a paused timer.

### properties

timer.elapsed
Set or get the elapsed in MS of the timer.

## Misc
dlg(text,callback=None)
show a square dialog. press arrows to repeat, enter to escape.
dlg_play(sound,callback=None,fade=False,fadespeed=30, context=None)
Play a sound and allow enter to interrupt it. You must supply a synthizer context object. Sound managers get a context that you can use, sound_manager.context.
grt(ms)
convert ms to a human readable time.
key_holding(key,delay=500,repeat=50)
see if a key is being pressed and then repeat if it is continued to be held down.
speak(text)
speak some text with the screen reader or SAPI.