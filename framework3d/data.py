# Encryption and game serialization functions written by Ivan Soto
import pickle as p
import hashlib
from Cryptodome.Cipher import AES
import os, platform, shutil

iv="flajef8ejri3l25m"

def directory_create(path):
	try:
		os.mkdir(path)
		return True
	except:
		return False


def directory_delete(path):
	try:
		os.rmdir(path)
		return True
	except:
		return False


def directory_exists(path):
	return os.path.isdir(path)


def file_exists(path):
	return os.path.isfile(path)


def find_recursive(path, wildcard='*.*'):
	files = []
	for r, d, f in os.walk(path):
		for file in f:
			if wildcard in file or wildcard == '*.*':
				files.append(os.path.join(r, file))

	return files


def find_directories(path):
	l = []
	for each in os.listdir(path):
		if os.path.isdir(each):
			l.append(each)

	return l


def file_copy(path, dest, overwrite=False):
	if overwrite == False:
		if os.path.isfile(path):
			pass
		return False
	else:
		shutil.copy(path, dest)
		return True


def file_delete(path):
	if os.path.isfile(path):
		os.remove(path)
		return True
	else:
		return False


def file_put_contents(filename, content, mode='a'):
	f = open(filename, mode)
	f.write(content)
	f.close()


def file_get_contents(filename, mode='rb'):
	ret = ''
	f = open(filename, mode)
	ret = f.read()
	f.close()
	return ret

def encrypt(data, key):
	try:
		key = key.encode('utf-8')
	except AttributeError:
		pass

	try:
		data = data.encode('utf-8')
	except AttributeError:
		pass

	encryptor = AES.new(hashlib.sha256(key).digest(), AES.MODE_CFB, iv.encode('utf-8'))
	return encryptor.encrypt(data)


def decrypt(data, key):
	try:
		key = key.encode('utf-8')
	except AttributeError:
		pass

	decryptor = AES.new(hashlib.sha256(key).digest(), AES.MODE_CFB, iv.encode('utf-8'))
	decryptedData = decryptor.decrypt(data)
	return decryptedData

class savedata(object):

	def __init__(self, filename, encrkey=''):
		self.fn = filename
		self.key = encrkey
		self.dic = dict()

	def exists(self, what):
		return what in self.dic

	def add(self, item, value):
		self.dic[item] = value

	def get(self, item):
		if self.exists(item) == False:
			return
		else:
			return self.dic[item]

	def save(self):
		if self.key != '':
			pd = encrypt(p.dumps(self.dic), self.key)
			file_put_contents(self.fn, pd, 'wb')
		else:
			pd = p.dumps(self.dic)
			file_put_contents(self.fn, pd, 'wb')

	def load(self):
		if file_exists(self.fn) == False:
			return ''
		if self.key != '':
			self.dic = p.loads(decrypt(file_get_contents(self.fn, 'rb'), self.key))
		else:
			self.dic = p.loads(file_get_contents(self.fn, 'rb'))
