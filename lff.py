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
	







GLYHEAD_OFFSET = 0x046
IMGDATA_OFFSET = 0xC66 


def make_glyph(charcode):
	gly = Record()
	gly.charcode = charcode
	gly.bearing_x = None
	gly.max_x = None
	gly.advance = None
	gly.bearing_y = None
	gly.max_y = None
	gly.segment = None
	gly.offset = None
	gly.flags = None
	gly.zero = None
	gly.bitmap = None
	return gly


def get_glyph_box(gly):	
	width = gly.max_x - gly.bearing_x
	height = gly.max_y + gly.bearing_y	
	return (gly.bearing_x, gly.bearing_y - height), (width, height)
			
def get_glyph_byte_dim(gly):
	width = gly.max_x - gly.bearing_x
	width_bytes = (width + 7) // 8
	height = gly.max_y + gly.bearing_y
	return width_bytes, height
	

			
			
def save_glyph(f, gly):
	f.write("charcode {}\n".format(gly.charcode))
	f.write("bearing_x {}\n".format(gly.bearing_x))
	f.write("max_x {}\n".format(gly.max_x))
	f.write("advance {}\n".format(gly.advance))
	f.write("bearing_y {}\n".format(gly.bearing_y))
	f.write("max_y {}\n".format(gly.max_y))
	f.write("flags {}\n".format(gly.flags))
	f.write("bitmap\n")
	f.write(gly.bitmap)
	f.write("%\n\n")
	

def read_glyph_header(f, gly):
	f.seek(GLYHEAD_OFFSET + (gly.charcode - 32) * 16)
			
	gly.bearing_x = read_int16(f)
	gly.max_x     = read_int16(f)
	gly.advance   = read_int16(f)
	gly.bearing_y = read_int16(f)
	gly.max_y     = read_int16(f)
	gly.segment   = read_uint16(f)
	gly.offset    = read_uint16(f)
	gly.flags     = read_uint8(f)
	gly.zero      = read_uint8(f)

	return gly



def read_lff(lff_name):
	""" LEGSHIP font files: TMB10, TMR10, TMR14, TMB12, TMR12, HVR08
	"""
	
	# bearing_x    positive right
	# bearing_y    positive up
	# max_x      positive right
	# max_y      positive down
	
	
	glys = []
	
	with open(lff_name, mode='rb') as f:

		for charcode in range(32, 32 + 194):
		
			gly = make_glyph(charcode)
		
			read_glyph_header(f, gly)
			read_glyph_bitmap(f, gly)
			
			glys.append(gly)


	oname = lff_name+'.txt'
	with open(oname, mode='w', encoding='utf-8') as f:
		for gly in glys:
			save_glyph(f, gly)
				
	print(oname)
	

		
def read_glyph_bitmap(f, gly):
	f.seek(IMGDATA_OFFSET + gly.offset)
	
	byte_width, byte_height = get_glyph_byte_dim(gly)
	_, dim = get_glyph_box(gly)
	
	bitmap = io.StringIO()
	
	for _j in range(byte_height):
		x = 0
		for _i in range(byte_width):
			# 1 byte -> 8 pix
			byte = f.read(1)[0]
			
			for k in range(7,-1,-1):
				if x < dim[0]:
					pix = (byte >> k) & 1
					
					if pix:
						bitmap.write("#")
						
					else:
						bitmap.write(".")
						
				x += 1
								
		bitmap.write("\n")
		
	gly.bitmap = bitmap.getvalue()
	
	







def load_glyph(f, gly):
	
	for cmd in ["charcode", "bearing_x", "max_x", "advance", "bearing_y", "max_y", "flags", "bitmap"]:
		
		xs = f.readline().strip().split()	
		
		if xs[0] != cmd:
			fail("expected command: {}; got: {}; charcode = {}; offset = {}", cmd, xs[0], gly.charcode, hex(f.tell()))
			
		if gly[cmd] != None:
			fail("{} already defined; charcode = {}; offset = {}", cmd, gly.charcode, hex(f.tell()))
			
		if cmd != 'bitmap':
			gly[cmd] = xs[1]
		else:
			load_glyph_bitmap(f, gly)
	
	
def load_glyph_bitmap(f, gly):
	bitmap = io.StringIO()
	while 1:
		c = f.read(1)
		
		if c in '#.':
			bitmap.write(c)		
		elif c in ' \t\r\n':
			pass
		elif c in '%':
			break
		else:
			fail("unexpected character while reading bitmap for charcode {}: {}", gly.charcode, repr(c))
	
	gly.bitmap = bitmap.getvalue()	
			


def write_lff(lff_name):

	glys = []
	with open(lff_name + '.txt', encoding='utf-8') as f:
		gly = make_glyph(None)
		load_glyph(f, gly)
		glys.append(gly)
		
	# calc data section size
	
	# TODO	
		
