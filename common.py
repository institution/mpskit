import struct, os, os.path, sys, io

class Error(Exception): 
	pass

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
	f.write(struct.pack(fmt, *ts))
	
def read_uint8(f):
	return read_struct(f, '<B')[0]
		
def read_uint16(f):
	return read_struct(f, '<H')[0]

def read_uint32(f):
	return read_struct(f, '<I')[0]
	
def read_int32(f):
	return read_struct(f, '<i')[0]
	
	
def write_uint8(f, val):
	return write_struct(f, '<B', (val,))
	
def write_uint16(f, val):
	return write_struct(f, '<H', (val,))

def write_uint32(f, val):
	return write_struct(f, '<I', (val,))
		
def write_int32(f, val):
	return write_struct(f, '<i', (val,))
	
