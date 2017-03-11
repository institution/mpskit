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
from common import *
from PIL import Image, ImageDraw
from PIL.ImagePalette import ImagePalette


def vga_color_trans(x):
	return int((x * 255) / 63)



def attach_palette(img, pal):
	R,G,B = [],[],[]
	for c in pal:
		R.append(c[0])
		G.append(c[1])
		B.append(c[2])

	img.putpalette(
		ImagePalette(
			mode = 'RGB', 
			palette = R + G + B, 		
			size = len(pal) * 3,
		)
	)
	




def export_palette(pal, name_ss):

	img = Image.new('P', (16,16), 0)

	attach_palette(img, pal)
	
	d = ImageDraw.ImageDraw(img)
	d.rectangle((0, 0, 16, 16), fill=0)
	for k in range(len(pal)):
		i = k % 16
		j = k // 16
		d.rectangle((i, j, i+1, j+1), fill=k)
		
	name_pal = '{}.pal.png'.format(name_ss)
	img.save(name_pal)
	print(name_pal)




def read_palette_col(f):
	""" Read palette as encoded in Colonization	
	repeat 256 
		uint8 r
		uint8 g
		uint8 b	
	"""
	
	pal = []

	for i in range(256):
		rr,gg,bb = reads(f, '3b')
		r,g,b = map(vga_color_trans, [rr,gg,bb])		
		pal.append((r,g,b))
		
	return pal


def read_palette_rex(f):
	"""	Read palette as encoded in Rex	
	uint16 ncolors
	repeat ncolors 
		uint8 red6
		uint8 green6
		uint8 blue6
		uint8 ind
		uint8 u2
		uint8 flags		
	"""
	
	ncolors = read_uint16(f)

	pal = []

	for i in range(ncolors):
		rr,gg,bb,ind,u2,flags = reads(f, '6b')
		r,g,b = map(vga_color_trans, [rr,gg,bb])
		
		#print("pal",rr,gg,bb,ind,u2,flags)
		
		# TODO: not the case in SECTION5/RM505A8.SS
		if ind != -1:
			warning("palette index != -1 (ignored); ind={}", ind)
		
		#assert pal[i] is None
		pal.append((r,g,b))
		
	assert len(pal) == ncolors
		
	return pal
