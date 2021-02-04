from accessible_output2.outputs import auto
speech_output=auto.Auto()
def speak(text,interrupt=True):
	speech_output.braille(text)
	return speech_output.output(text,interrupt)