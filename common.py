""" Copyright 2015  Institution, sta256+mpskit at gmail.com
    
    This file is part of mpskit.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY.

    See LICENSE file for more details.
"""

from io import BytesIO
import json
import struct, os, os.path, sys, io
from collections import OrderedDict
import _io, sys



class Error(Exception): 
	def __str__(self):
		return format(*self.args)
	
class External(Error): pass
class InvalidMadspackVersion(Error): pass










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


def read_until(f, b=0):	
	xs = []
	while 1:
		x = read_uint8(f)
		xs.append(x)
		#import ipdb; ipdb.set_trace()
		if x == b:
			break
			
	return bytes(xs)
	
	
def get_asciiz(buf):	
	i = buf.find(b'\x00')
	return buf[:i].decode('ascii')

def write_struct(f, fmt, ts):	
	return f.write(struct.pack(fmt, *ts))
	#return struct.calcsize(fmt)
	

def read_raw(f, n):
	return [x for x in f.read(n)]
	#return read_struct(f, '<B')[0]


def write_raw(f, n, bs):
	assert len(bs) == n
	i = 0
	for b in bs:
		assert 0 <= b < 256
		write_uint8(f, b)
		i += 1
	return i

def check_ext(name, ext):
	if not name.upper().endswith(ext.upper()):
		error('invalid extension: expected={}; file={};', ext, name)

def read_raw(f, n):
	return f.read(n)
	#return [x for x in f.read(n)]
	#return read_struct(f, '<B')[0]


def write_raw(f, n, bs):
	assert len(bs) == n
	i = 0
	for b in bs:
		assert 0 <= b < 256
		write_uint8(f, b)
		i += 1
	return i

def decode_buffer(xs):
	return xs.decode('latin1')
	
		
def encode_buffer(xs):
	return xs.encode('latin1')
		

	
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
	



def write_ascii(f, s):
	for b in s.encode('ascii'):
		write_uint8(f, b)

def error(fmt, *args):
	print('ERROR: ' + fmt.format(*args))
	sys.exit(1)

def warning(fmt, *args):
	print('WARNING: ' + fmt.format(*args))
	

def write_string(f, n, s):
	if len(s) > n:
		error('string too long (must be < {}): {}', n, s)
				
	for ch in s:
		byte = ord(ch)
		assert 0 <= byte <= 255
		write_uint8(f, byte)
			
	return n




def decode_string(b, null_term=False):
	"""
	null_term -- strip null and anything past it
	"""
	assert isinstance(b, (bytes, list))
	
	xs = []
	for byte in b:		
		if null_term and byte == 0:
			break
		assert (0 <= byte < 128)
		#import ipdb; ipdb.set_trace()
		xs.append(chr(byte))
		
	s = ''.join(xs)
	s = s.replace("\x00", '|')
	return s
		
def encode_string(s, null_term=False, max_len=None, fill=False):
	"""
	null_term -- add null at the end of string if not already present
	max_len -- raise error when string is longer then max_len after encoding
	fill -- fill to max_len with nulls
	"""	
	if null_term and not s.endswith('|'):
		s = s + '|'		
	s = s.replace('|', "\x00")
	b = s.encode('ascii')
	
	if max_len is not None and len(b) > max_len:
		error('this string must be shorter then {} chars: {}', max_len, s)
	
	if fill:
		b = b + b''.join([b'\x00'] * (max_len - len(b)))
	return b



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
	
	def as_dict(self):
		return self.__dict__['_inner']
	
		
	def as_list(self):
		return self.__dict__['_inner']
		
		ls = []
		for k,v in self.items():
			ls.append((k,v))
		return ls

	@classmethod
	def from_dict(Cls, kvs):
		r = Cls()
		r.__dict__['_inner'] = kvs
		return r


	@classmethod
	def from_list(Cls, kvs):
		r = Cls()
		for k,v in kvs.items():
			r[k] = v
		return r


Header = Record
