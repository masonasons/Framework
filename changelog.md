# 2.0
* Switches to Synthizer for sound handling code. The way this works is pretty ugly right now.
* Splits code up into many files.
* Possibly going open source? IDK.
* Fixes many bugs/inconsistancies.

# 0.x-1.0
* Undocumented changes, renames to framework and removes window functions, those are now handled by Lucia.


# Older versions

# 0.28
* Now using Kianoosh's sound pool (Thanks Kianoosh!)

# 0.27
* renames window_flush to flush_window for the sake of consistency, because every other window-related func is x_window, not window_x.
* adds is_playing and is_active to sound pool.
* New functions from Ivan

# 0.26
* Some unofficial/broken functions removed.

# 0.25
* Modifications to pack file to work under Linux. Requires recompile of sounds.

# 0.24
* adds clear method to map class
* Adds map class!

# 0.23
* Adds dl_file function.

# 0.22
* Make listener_angle optional in 2d and 3d.

# 0.21
* Adds pgt_credits and pgt_version vars.
* Adds tempo and tempo_pitch variable to sound.

# 0.2
* Adds effects to sound class.

# 0.14
* Just for fun, replaced ogg sounds with Opus ones, decreasing size by 200 KB
* Now you have example bat file for EXE compilation. If you don't put the hook file in your hooks folder, expect this to fail hard.
* Now performing UPX compression. Size goes down from 400 kb to 98 kb. Boom!
* PGT is now cythonized! Source is in src folder, with tools needed to compile. Still need vs. When using, copy pgt.pyd, not py. Still need pack.py.

# 0.13
* Fade function in sound_pool's destroy_all def.
* panning in menues now defaults to false
* added the fade function to menu that optionally takes 2 parameters: end that defaults to -40, and time that defaults to self.fade_time

# 0.12
* changed the while loop in the dlg_play function to allow the function to die when the sound has finished playing rather than still waiting for you to press enter
* Adds sleep to all functions that wait for user input (Menu, dlg, etc)

# 0.11
* Menu.add_item_tts now has the disable perametor to disable menu items.