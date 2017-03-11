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
from madspack import read_madspack, write_madspack, save_madspack
from PIL import Image
from palette import read_palette_col, attach_palette

"""
PIK (Colonization)
MADSPACK
Section 0: Header
Section 1: Image (8bit indexed)
Section 2: Palette
"""

def read_pik(pik_name):
	check_ext(pik_name, '.PIK')
	
	parts = read_madspack(pik_name)
	assert len(parts) >= 3
	save_madspack(pik_name, parts)
	
	h = read_pik_header(parts[0])	
	pal = read_palette_col(parts[2])
	img = read_pik_image(parts[1], h, pal)
		
	save_image(pik_name, img)
	

def read_pik_header(f):
	h = Header()
	h.height = read_uint16(f)
	h.width = read_uint16(f)
	h.unk1 = read_uint16(f)
	h.unk2 = read_uint16(f)
	return h


def read_pik_image(part, h, pal):
	
	img = Image.new('P', (h.width, h.height))
	attach_palette(img, pal)
	pix = img.load()	
	 
	for j in range(h.height):
		for i in range(h.width):
			pix[i,j] = read_uint8(part)

	return img




