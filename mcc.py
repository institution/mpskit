""" Copyright 2015-2017  sta256+mpskit at gmail.com
    
    This file is part of mpskit.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY.

    See LICENSE file for more details.
"""
from common import *
from PIL import Image, ImageDraw
from palette import attach_palette
import sys, struct, io
	

pal = [
	[0x0,0x0,0x0],
	[0x7d,0x7d,0x7d],
	[0x41,0x41,0x41],
	[0xeb,0xcf,0x9e],
	[0xff,0xff,0xff],
	[0x82,0x61,0x0],
	[0xff,0x0,0x0],
	[0x0,0x8,0x28],
	[0x4,0x20,0x3c],
	[0xc,0x2c,0x49],
	[0x0,0x10,0x28],
	[0x14,0x34,0x55],
	[0x1c,0x41,0x61],
	[0xb6,0xb6,0xb6],
	[0x5d,0x5d,0x5d],
	[0x1c,0x1c,0x1c],	
]

def make_sprite(name):
	h = Record()
	h.name = name
	h.bitmap_offset = None
	h.unk0 = None
	h.width = None
	h.height = None
	h.bitdepth = None
	h.unk2 = None
	h.unk3 = None
	h.bitmap = None
	return h


def get_byte_width(width, bitdepth):
	assert bitdepth in (4,8)
	k = 8 / bitdepth
	return (width + k - 1) // k
			
			
def get_sprite_path(s, mcc_name):
	opath = mcc_name + '.dir/' + s.name.lower().strip('.').replace('\\', '/') + '.png'	
	return opath
			
def save_sprite(s, mcc_name):
	assert s.name
	assert s.bitmap
	
	opath = get_sprite_path(s, mcc_name)
	odir,oname = os.path.split(opath)
	os.makedirs(odir, exist_ok=True)	
	s.bitmap.save(opath)
	print(opath)



def read_sprite_header(f, index, s):
	f.seek(index * 4)
	header_offset = read_uint32(f)
	f.seek(header_offset)
	

	
	s.bitmap_offset = read_uint32(f)
	s.unk0 = read_int16(f)
	s.width = read_int16(f)
	s.height = read_int16(f)
	s.bitdepth = read_int16(f)
	s.unk2 = read_int16(f)
	s.unk3 = read_int16(f)
	
	assert f.tell() == header_offset + 16
	
	return s

def iter_mcc(f):
	while 1:
		x = f.read(1)
		if len(x) == 0 or x[0] == 0xFF:
			return
		
		bs = x + f.read(29)
		yield bs.decode('ascii')
		
		# skip newline
		f.read(2) 
		

def read_mcc(mcc_name):
	wmcc_name = 'W{}.MCC'.format(mcc_name)
	with open(mcc_name, 'rb') as mcc:
		with open(wmcc_name, 'rb') as wmcc:
			for i,line in enumerate(iter_mcc(mcc)):
				
				s = make_sprite(line)
				read_sprite_header(wmcc, i, s)	
				
				if s.bitdepth == 4:
					read_sprite_bitmap(wmcc, s)	
					save_sprite(s, mcc_name)
					
				else:
					# not implemented
					pass
	

def write_mcc(mcc_name):	
	wmcc_name = 'W{}.MCC'.format(mcc_name)
	ss = []
	with open(mcc_name, 'rb') as mcc:
		with open(wmcc_name, 'rb') as wmcc:
			for i,line in enumerate(iter_mcc(mcc)):
				
				s = make_sprite(line)
				read_sprite_header(wmcc, i, s)
				
				if s.bitdepth == 4:
					load_sprite_bitmap(s, mcc_name)					
					
					ss.append(s)
					
					
				else:
					# not implemented
					pass
	
	
	
	with open(wmcc_name, 'r+b') as wmcc:
		for s in ss:
			write_sprite_bitmap(wmcc, s)
			
								
	print(wmcc_name)
				
def load_sprite_bitmap(s, mcc_name):
	path = get_sprite_path(s, mcc_name)
	s.bitmap = Image.open(path)
	
def write_sprite_bitmap(f, s):
	pix = s.bitmap.load()
	
	f.seek(s.bitmap_offset + 2)
	assert f.tell() == s.bitmap_offset + 2
	
	
	mask = 0xFF >> (8 - s.bitdepth)
	for y in range(s.height):				
		
		byte = 0x00
		
		shift = 8
		for x in range(s.width):
		
			shift -= s.bitdepth
			
			c = pix[x,y]
			
			byte |= (c << shift)
					
			if shift == 0:
				write_uint8(f, byte)
				shift = 8
				byte = 0x00
		
		if shift != 8:
			write_uint8(f, byte)
			byte = 0x00
		

	
	byte_size = get_byte_width(s.width, s.bitdepth) * s.height
	assert f.tell() - s.bitmap_offset - 2 == byte_size, (f.tell() - s.bitmap_offset - 2, byte_size)
	

def read_sprite_bitmap(f, s):
	
	dim = (s.width, s.height)
	img = Image.new('P', dim)
	pix = img.load()
	
	attach_palette(img, pal)

	f.seek(s.bitmap_offset + 2)
	
	mask = 0xFF >> (8 - s.bitdepth)
	
	for y in range(s.height):				
		
		shift = 0
		for x in range(s.width):
		
			if shift == 0:
				byte = f.read(1)[0]
				shift = 8
		
			shift -= s.bitdepth
			
			color = (byte >> shift) & mask
				
			pix[x,y] = color

	s.bitmap = img

	
	byte_size = get_byte_width(s.width, s.bitdepth) * s.height
	assert f.tell() == s.bitmap_offset + 2 + byte_size
		
	
	
