from io import BytesIO
import json
import struct, os, os.path, sys, io
from collections import OrderedDict
import _io, sys



class Error(Exception): pass
class External(Error): pass

g_curr_dir = ''

def open2(name,flags):
	if isinstance(name,_io._IOBase):		
		return name
	else:
		return open(name,flags)

def output(fname):
	print(os.path.join(g_curr_dir, fname))
	


def read_idstring(f, idstring):
	x = f.read(len(idstring))
	if x != idstring:
		raise Error("invalid idstring: {}; expected={};  ".format(repr(x), repr(idstring)))

def check_magic(x, y):
	if x != y:
		raise Error("invalid magic: {} != {};  ".format(repr(x), repr(y)))

verbose = 1

	
def read_struct(f, fmt):
	data = f.read(struct.calcsize(fmt))
	return struct.unpack(fmt, data)
	
def calcsize(fmt):
	return struct.calcsize(fmt)
	
reads = read_struct

def read(f, fmt):
	return read_struct(f,fmt)[0]
	
def get_asciiz(buf):	
	i = buf.find(b'\x00')
	return buf[:i].decode('ascii')

def write_struct(f, fmt, ts):	
	return f.write(struct.pack(fmt, *ts))
	#return struct.calcsize(fmt)
	

def read_bytes(f, n):
	return [x for x in f.read(n)]
	#return read_struct(f, '<B')[0]


def read_ascii(f, n):
	ls = []
	for _ in range(n):
		ls.append(chr(read_uint8(f)))
	return ''.join(ls)
	
read_string = read_ascii
	
def read_uint8(f):
	return read_struct(f, '<B')[0]
		
def read_uint16(f):
	return read_struct(f, '<H')[0]

def read_sint16(f):
	return read_struct(f, '<h')[0]


def read_uint32(f):
	return read_struct(f, '<I')[0]
	
def read_int32(f):
	return read_struct(f, '<i')[0]

	
def write_uint8(f, val):
	write_struct(f, '<B', (val,))
	return 1
	
def write_uint16(f, val):
	return write_struct(f, '<H', (val,))

def write_sint16(f, val):
	return write_struct(f, '<h', (val,))

def write_uint32(f, val):
	return write_struct(f, '<I', (val,))
		
def write_int32(f, val):
	return write_struct(f, '<i', (val,))
	

def write_bytes(f, bs):
	i = 0
	for b in bs:
		assert 0 <= b < 256
		write_uint8(f, b)
		i += 1
	return i


def write_ascii(f, s):
	for b in s.encode('ascii'):
		write_uint8(f, b)

def write_string(f, n, s):
	if len(s) > n:
		print('ERROR: string too long (must be < {}):'.format(n), s)
		sys.exit(2)
		
	for ch in s:
		byte = ord(ch)
		assert 0 <= byte <= 255
		write_uint8(f, byte)
	
	# null fill
	for _ in range(n - len(s)):
		write_uint8(f, 0)
		
	return n
		
		


class Record:
	def __init__(self):
		self.__dict__['_inner'] = OrderedDict()
		
	def __setattr__(self,k,v):			
		self.__dict__['_inner'][k] = v
		
	def __getattr__(self,k):
		return self.__dict__['_inner'][k]
		
	def __setitem__(self,k,v):			
		self.__dict__['_inner'][k] = v
	
	def __getitem__(self,k):			
		return self.__dict__['_inner'][k]	
		
	def items(self):		
		return self._inner.items()
		
	def as_list(self):
		ls = []
		for k,v in self.items():
			ls.append((k,v))
		return ls

	@classmethod
	def from_list(Cls, kvs):
		r = Cls()
		for k,v in kvs:			
			r[k] = v
		return r


Header = Record
