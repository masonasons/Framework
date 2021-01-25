from cytolk import tolk
tolk.load()
def speak(text,interrupt=True):
	return tolk.output(text,interrupt)
