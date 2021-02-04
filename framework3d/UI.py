import pyperclip
import platform
from fw import speech

import pygame
import string
import time

WHITELIST_ALL = [i for i in string.printable if not i == "\r" or i == "\n"]
WHITELIST_LETTERS = [i for i in string.ascii_letters]
WHITELIST_DIGITS = [i for i in string.digits]
WHITELIST_HEXDIGITS = [i for i in string.hexdigits]
WHITELIST_NEGDIGITS = WHITELIST_DIGITS + ["-"]
WHITELIST_FLOATDIGITS = WHITELIST_DIGITS + ["."]
WHITELIST_NEGFLOATDIGITS = WHITELIST_FLOATDIGITS + ["-"]


class VirtualInput:
	def __init__(
		self, message="", password=False, whitelist=WHITELIST_ALL, value="", callback=None, hidden_message = "Hidden"
	):
		self.text = value
		self.message = message
		self.password = password
		self.callback = callback
		# set by the callback and used to break out of the input loop at any given time
		self.input_break = False
		self.allowed_characters = whitelist
		#cursor
		self.charindex=0
		self.password_message = hidden_message

	def run(self):
		speech.speak(self.message)
		while True:
			time.sleep(0.001)
			if callable(self.callback):
				self.callback(self)
			if self.input_break:
				break
			events = window.process_events()
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.charindex = 0
						self._output_char(self.text, True)
					elif event.key == pygame.K_DOWN:
						self.charindex = len(self.text)
						self._output_char(self.text, True)
					elif event.key == pygame.K_HOME:
						self.charindex = 0
						if len(self.text)>0:
							self._output_char(self.text[0])
					elif event.key == pygame.K_END:
						self.charindex = len(self.text)
						speech.speak("Blank")
					elif event.key == pygame.K_LEFT and len(self.text)>0:
						if self.charindex > 0:
							self.charindex-=1
						elif self.charindex <= 0:
							self.charindex=0
						self._output_char(self.text[self.charindex])
					elif event.key == pygame.K_RIGHT and len(self.text)>0:
						if self.charindex < len(self.text):
							self.charindex+=1
							if self.charindex >= len(self.text):
								self.charindex=len(self.text)
								#using the default speaking function, to prevent from saying the hidden_message instead of blank when in a password field.
								speech.speak("blank")
							elif self.charindex <= len(self.text)-1:
								self._output_char(self.text[self.charindex])
						else:
							speech.speak("blank")
					elif event.key == pygame.K_BACKSPACE:
						if len(self.text) == 0 or self.charindex <= 0:
							continue
						what = self.text[self.charindex-1]
						temp=""
						if self.charindex < len(self.text):
							temp=self.text[:self.charindex-1]+self.text[self.charindex:]
						elif self.charindex == len(self.text):
							temp=self.text[:self.charindex-1]
						self.text=temp
						self.charindex-=1
						self._output_char(what)
					elif event.key == pygame.K_RETURN:
						return self.text
					elif event.key == pygame.K_SPACE:
						if self.charindex < len(self.text):
							self.text = self.text[:self.charindex] + " " + self.text[self.charindex:]
							self.charindex += 1
						elif self.charindex == len(self.text):
							self.text += " "
							self.charindex+=1
						self._output_char(" ")
					else:
						try:
							if event.unicode in self.allowed_characters and window.key_down(pygame.K_LCTRL)==False and window.key_down(pygame.K_RCTRL)==False:
								if self.charindex < len(self.text):
									self.text = self.text[:self.charindex] + event.unicode + self.text[self.charindex:]
									self.charindex += 1
								elif self.charindex == len(self.text):
									self.text += event.unicode
									self.charindex+=1
								self._output_char(event.unicode)
						except ValueError:
							continue

	def _output_char(self, char, speak_number=False):
		to_speak = ""
		if self.password:
			to_speak += self.password_message
			if speak_number:
				to_speak += f" {len(self.text)} characters"
		else:
			if char == " ":
				to_speak += "space"
			else:
				to_speak += char
		speech.speak(to_speak)

def input_callback(input):
	if window.key_down(pygame.K_LCTRL) or window.key_down(pygame.K_RCTRL):
		if window.key_pressed(pygame.K_v):
			result=pyperclip.paste()
			input.text = input.text[:input.charindex] + result + input.text[input.charindex:]
			speech.speak("Pasted")

def input_box(parent=None, message="", caption="", default_value=""):
	if platform.system()=="Darwin":
		speech.speak(caption)
	i=VirtualInput(caption,callback=input_callback)
	result=i.run()
	if result==None:
		return ""
	return result