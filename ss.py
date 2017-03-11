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
from madspack import read_madspack, write_madspack, save_madspack
from collections import namedtuple
from PIL import Image, ImageDraw
from fab import read_fab
from palette import read_palette_col, read_palette_rex, attach_palette, export_palette

ext = 'png'

transparency_index = 0xFD

FEATURE_RESIZE = 1

def read_ss(f, ss_name):
	
	"""
	SS file is a MADSPACK file with 4 parts:

	* part 0
		header
			mode -- part3 encoding
				0 -- linemode
				1 -- FAB and linemode
			count -- number of sprites
			size -- size of part3
		
		
	* part 1
		is composed of tile_headers, there can be many tiles in one file 
		ntiles = len(part2) / 0x00000010

	* part 2
		palette
		
	* part 3	
		image data, may contain many tiles


	Tiles are compressed with linemode|command encoding. Colors are stored
	in indexed mode. Each pixel line begins with linemode. 

	Linemodes/commands:
	lm  cm            description
	------------------------------------------------------------------------
	255               fill rest of the line with bg color and read linemode

	252               stop

	254               pixel mode
	254 255           fill rest of the line with bg color and read linemode
	254 254 len col   produce len * [col] pixels, read command
	254 col           produce [col] pixel, read command

	253               multiple pixels mode
	253 255           fill rest of the line with bg color and read linemode
	253 len col       produce len * [col] pixels, read command

	"""
	check_ext(ss_name, '.SS')
		
	verbose = 0
	
	
	parts = read_madspack(f)
	
	save_madspack(ss_name, parts)
		
	ss_header = read_ss_header(parts[0])
	
	# save header
	save_ss_header(ss_name, ss_header)
	
	if verbose:
		print("nsprites=", ss_header.nsprites)
	
		
	sprite_headers = []
	
	for i in range(ss_header.nsprites):
		sprite_header = read_sprite_header(parts[1])
		sprite_headers.append(sprite_header)
		
		# save header
		sprite_name = '{}.{:03}'.format(ss_name, i)
		save_sprite_header(sprite_name, sprite_header)
		
	
	if ss_header.pflag:
		# print("PFLAG IS ON")
		pal = read_palette_col(parts[2])
	else:
		pal = read_palette_rex(parts[2])
	
	export_palette(pal, ss_name)

	
	
	
	sprites = []
	for i, sprite_header in enumerate(sprite_headers):
		sprite = read_sprite(sprite_header, parts[3], pal, mode = ss_header.mode)
		sprites.append(sprite)
		
		# save sprite
		sprite_name = '{}.{:03}'.format(ss_name, i)
		
		save_image(sprite_name, sprite, transparency=transparency_index)
	
	return sprites


	



def write_ss(ss_name):
	check_ext(ss_name, '.SS')
		
	ss_header = load_ss_header(ss_name)
	
	
	# palette
	part2 = open('{}.s02.part'.format(ss_name), 'rb')
	
	if ss_header.pflag:
		#print("PFLAG IS ON")
		pal = read_palette_col(part2)
	else:
		pal = read_palette_rex(part2)
	
	# reverse palpalettelete
	rpal = {}
	for i,col in enumerate(pal):
		rpal[col] = i
	
		
	part1 = BytesIO()
	part3 = BytesIO()
		
	size = 0
	for i in range(ss_header.nsprites):		
		sprite_name = '{}.{:03}'.format(ss_name, i)		
		img = Image.open(sprite_name+'.png')		
		spr_hd = load_sprite_header(sprite_name)		
		size += write_sprite(part1, part3, spr_hd, img, rpal)
		
		
	ss_header.mode = 0   # only linemode without fab
	ss_header.data_size = size
	
	part0 = BytesIO()
	write_ss_header(part0, ss_header)
	
	
	parts = [part0, part1, part2, part3]
	
	for part in parts:
		part.seek(0)
	
	write_madspack(ss_name, parts)
		
	print(ss_name)
	
	
		

	

def save_sprite_header(sprite_name, h):
	oname = sprite_name + '.json'
	with open(oname, 'w') as f:
		json.dump(h.as_dict(), f, indent=2)
	
	print(oname)
	


def load_sprite_header(sprite_name):
	with open('{}.json'.format(sprite_name), 'r') as f:
		return Header.from_dict(json.load(f))
	

		
def load_ss_header(ss_name):
	with open('{}.json'.format(ss_name), 'r') as f:
		return Header.from_dict(json.load(f))
	

def save_ss_header(ss_name, h):
	oname = ss_name + '.json'
	with open(oname, 'w') as f:
		json.dump(h.as_dict(), f, indent=2)	
	print(oname)

def read_ss_header(f):
	h = Header()	
	h.mode = read_uint8(f)
	h.unk1 = read_uint8(f)
	h.type1 = read_uint16(f)
	h.type2 = read_uint16(f)
	
	h.unk2a = decode_buffer(read_raw(f, 6))
	h.pflag = read_uint8(f)
	h.unk2b = decode_buffer(read_raw(f, 25))	
	
	assert f.tell() == 0x26
	h.nsprites = read_uint16(f)  
	h.unk3 = decode_buffer(read_raw(f, 108))
	assert f.tell() == 0x94
	h.data_size = read_uint32(f)   # size of last section (part) (unfabed)
	assert f.tell() == 0x98
	return h




def write_ss_header(f, h):
	write_uint8(f, h.mode)
	write_uint8(f, h.unk1)
	write_uint16(f, h.type1)
	write_uint16(f, h.type2)
	write_raw(f, 6, encode_buffer(h.unk2a))
	write_uint8(f, h.pflag)
	write_raw(f, 25, encode_buffer(h.unk2b))	
	assert f.tell() == 0x26
	write_uint16(f, h.nsprites) 
	write_raw(f, 108, encode_buffer(h.unk3))
	assert f.tell() == 0x94
	write_uint32(f, h.data_size)   # size of last section (part) (unfabed)
	assert f.tell() == 0x98
	return f.tell()
	



def write_sprite_header(f, h):	
	write_uint32(f, h.start_offset)
	write_uint32(f, h.length)
	
	# probably margins; seems unused most of the time
	write_uint16(f, h.width_padded)
	write_uint16(f, h.height_padded)
	
	# image size
	write_uint16(f, h.width)
	write_uint16(f, h.height)
	
def read_sprite_header(f):
	verbose = 0
	
	h = Header()
	
	h.start_offset = read_uint32(f)
	h.length = read_uint32(f)
	h.width_padded = read_uint16(f)
	h.height_padded = read_uint16(f)
	h.width = read_uint16(f)
	h.height = read_uint16(f)
	
	
	if verbose:
		print('padded=', (h.width_padded, h.height_padded))
		print('normal=', (h.width, h.height))
	

	return h


	
	

	
	
	
	
	
	



	
def write_sprite(head, data, header, img, rpal):
	"""
	head -- headers part
	data -- data part
	header -- original header
	img -- image
	rpal -- reversed palette	
	return -- size writen to data
	
	
	Tiles are compressed with linemode|command encoding. Colors are stored
	in indexed mode. Each pixel line begins with linemode. 

	Linemodes/commands:
	lm  cm            description
	------------------------------------------------------------------------
	255               fill rest of the line with bg color and read linemode

	252               stop

	254               pixel mode
	254 255           fill rest of the line with bg color and read linemode
	254 254 len col   produce len * [col] pixels, read command
	254 col           produce [col] pixel, read command

	253               multiple pixels mode
	253 255           fill rest of the line with bg color and read linemode
	253 len col       produce len * [col] pixels, read command

	253 len col
	
	
	"""

	def get_index(x,y):
		if img.mode == 'P':
			return img.getpixel((x,y))
		else:
			# backwards compability RGBA
			pix = img.getpixel((x,y))
			if pix == (0,0,0,0):
				# transparent background
				return 0xFD
			else:
				col = pix[:3]
				return rpal[col]
		
	
	# 1x1 image is used instead of 0x0 image because 0x0 image cannot be represented as png	
	if img.size[0] > 1 and img.size[1] > 1:
		header.width = img.size[0]
		header.height = img.size[1]
	
	#	if img.size[0] > 1:
	#		assert header.width == img.size[0]	
	#	if img.size[1] > 1:
	#		assert header.height == img.size[1]
	
	
	# data
	start = data.tell()
	size = 0
	for y in range(header.height):
		
		size += write_uint8(data, 253)     # multipixel line mode
		
		x = 0
		while x < header.width:
			
			ind0 = get_index(x,y)
			length = 0
			while x < header.width and length < 255:
				ind = get_index(x,y)
				if ind == ind0:
					length += 1
					x += 1
				else:
					break
					
			if length:
				size += write_uint8(data, length)
				size += write_uint8(data, ind0)
			
		size += write_uint8(data, 255)   # end of line
			
	size += write_uint8(data, 252)
			
	# header
	header.start_offset = start
	header.length = data.tell() - start
	
	write_sprite_header(head, header)	
	
	return size
				



	
def read_sprite(ti, rdata, pal, mode, verbose=0):
	"""
	ti -- sprite header
	rdata -- file-like object
	pal -- array of (R,G,B)
	"""
	
	rdata.seek(ti.start_offset)
	
	if mode == 0:
		data = rdata.read(ti.length)
	
	elif mode == 1:
		data = read_fab(rdata, ti.length).read()
		
	else:
		raise Error('invalid sprite mode: {}'.format(mode))
	
	
	
	# special case
	if ti.width == 0 or ti.height == 0:
		if data[0] == 252:		
			img = Image.new("P", (1,1))
			attach_palette(img, [(0,0,0)])			
			img.putpixel((0,0), 0)
			return img
		else:
			raise Error('invalid encoding of 0x0 image while reading SS file')
			

	img = Image.new('P', (ti.width, ti.height))
	attach_palette(img, pal)
	
	pix = img.load()
	
	if verbose:
		print("sprite size =", ti.width, ti.height)
	
	i = j = 0
	k = 0
	bg = 0xFD
	
	def write_ind(ci, l=1):
		if ci == bg:
			c = bg # 0?
		else:
			c = ci
			
		nonlocal i
		while l > 0:
			if verbose:
				print(i,j,c)
			pix[i,j] = c
			i += 1
			l -= 1
	
	def nextline():
		nonlocal i,j
		i = 0
		j += 1
	
	def read():
		nonlocal k
		r = data[k]
		k += 1
		return r
	
	
	def read_lm():
		x = read()
		if verbose:
			print('lm=',x)
		return x
			
			
	lm = read_lm()
	
			
	while 1:   #j < ti.height:  #k < ti.length:
		
		# line mode
		if lm == 255:
			# fill with bg color to the end of this line
			write_ind(bg, ti.width - i)
			nextline()
			lm = read_lm()
			
			
		elif lm == 252:
			# end of image
			break
			
		else:
			x = read()
			if x == 255:
				write_ind(bg, ti.width - i)			
				nextline()
				lm = read_lm()			
		
			else:
				if lm == 254:
					# pix			
					if x == 254:
						l = read()
						ci = read()
						write_ind(ci, l)
					
					else:
						write_ind(x)
					
				elif lm == 253: 
					ci = read()
					write_ind(ci, x)
				
				else:
					print('ERROR: unknown lm:', lm)
					assert 0
	
	
	return img
	

