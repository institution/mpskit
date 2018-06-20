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
from madspack import read_madspack, save_madspack, write_madspack
from PIL import Image
from palette import attach_palette
"""
FF file format

MADSPACK with 1 section

Section 0



one pix encoded on 2 bits, 4 possible colors


font_colors = []
font_colors[0] = 0xFF
font_colors[1] = 0x0F
font_colors[2] = 0x07
font_colors[3] = 0x08

"""

pal = [(0,0,0,0),(0,255,0,255),(0,127,0,255),(0,63,0,255)]

def get_col_index(img,c):
	if img.mode == 'P':
		return c
	elif img.mode == 'RGB':
		return get_col_index_RGB(c)
	elif img.mode == 'RGBA':
		return get_col_index_RGBA(c)
	else:
		fail("invalid font image mode: {}; should be 'P', 'RGB', or 'RGBA'", img.mode)

def get_col_index_RGB(c):
	if c == (0,0,0):
		return 0
	if c == (0,255,0):
		return 1
	if c == (0,127,0):
		return 2
	if c == (0,63,0):
		return 3
	fail("invalid font color: {}".format(c))


def get_col_index_RGBA(c):
	if c[:3] == (0,0,0):
		return 0
	if c == (0,255,0,255):
		return 1
	if c == (0,127,0,255):
		return 2
	if c == (0,63,0,255):
		return 3
	fail("invalid font color: {}".format(c))



def load_ff_header(ff_name):
	return Record.from_list(
		json.load(open("{}.json".format(ff_name)))
	)


def save_ff_header(ff_name, h):
	n = "{}.json".format(ff_name)
	open(n, 'w').write(json.dumps(h.as_list(), indent=2))
	output(n)

def write_ff(ff_name):
	check_ext(ff_name, '.FF')

	h = load_ff_header(ff_name)

	f = BytesIO()
	f.seek(2 + 128 + 256)

	for i in range(1,128):
		write_glyph(f, ff_name, h, i)

	f.seek(0)
	write_ff_header(f, h)
	assert f.tell() == 2 + 128 + 256

	write_madspack(ff_name, [f])



def write_glyph(f, ff_name, h, n):

	iname = "{}.{:03}.png".format(ff_name, n)
	if not os.path.exists(iname):
		h.char_widths[n] = 0
		h.char_offsets[n] = f.tell()

	else:
		img = Image.open(iname)

		width,height = img.size

		if h.max_width < width:
			h.max_width = width

		if h.max_height < height:
			h.max_height = height

		h.char_widths[n] = width
		h.char_offsets[n] = f.tell()

		y = 0
		while y < height:
			x = 0
			eol = False
			while not eol:
				byte = 0b00000000

				for shift in (6,4,2,0):
					ind = get_col_index(img, img.getpixel((x,y)))
					byte = byte | (ind << shift)

					x += 1
					if x == width:
						eol = True
						break

				write_uint8(f, byte)

			y += 1

def write_ff_header(f, h):
	write_uint8(f, h.max_height)
	write_uint8(f, h.max_width)

	assert f.tell() == 2

	for b in h.char_widths[1:]:
		write_uint8(f, b)
	write_uint8(f, 0)

	assert f.tell() == 2 + 128

	for o in h.char_offsets[1:]:
		write_uint16(f, o)
	write_uint16(f, 0)

	assert f.tell() == 2 + 128 + 256


def read_ff(ff_name):
	"""
	FF file: 1 part MADSPACK
	header
		max_height: 1 byte
		max_width: 1 byte
		glyphs widths: 128 bytes
		glyphs offsets: 2 x 128 byte
	glyphs
		...
	"""
	check_ext(ff_name, '.FF')

	parts = read_madspack(ff_name)
	save_madspack(ff_name, parts)
	f = parts[0]

	# Header
	h = Record()
	h.max_height = read_uint8(f)
	h.max_width = read_uint8(f)

	# glyphs width in pixels
	# glyph height is max_height
	# null has width 0
	h.char_widths = [0] + [read_uint8(f) for _ in range(127)]

	read_uint8(f)  # alignment to 128



	# space occupied by glyph is
	# math.ceil((glyph_width * max_height) / 4.0)   # or is is rounded per line ?

	# offsets inside section
	h.char_offsets = [2 + 128 + 256] + [read_uint16(f) for _ in range(127)]

	read_uint16(f)  # alignment

	assert f.tell() == 2 + 128 + 256


	save_ff_header(ff_name, h)

	# Glyphs

	f.seek(h.char_offsets[1])
	for ch in range(1,128):

		width = h.char_widths[ch]
		height = h.max_height
		offset = h.char_offsets[ch]

		assert f.tell() == offset

		if width == 0:
			continue

		img = Image.new("P", (width,height))
		attach_palette(img, pal)

		y = 0
		while y < height:
			x = 0
			while 1:
				byte = read_uint8(f)

				col = (byte & 0b11000000) >> 6
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break

				col = (byte & 0b00110000) >> 4
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break

				col = (byte & 0b00001100) >> 2
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break

				col = (byte & 0b00000011) >> 0
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break

			y += 1

		oname = "{}.{:03}.png".format(ff_name, ch)
		img.save(oname)
		output(oname)





def export_ftb(ff_name, scale=3):
	""" Export font to custom binary ftb format
	"""

	h = load_ff_header(ff_name)

	with open(ff_name+'.ftb', 'wb') as f:
		write_uint32(f, 0x46425446)
		write_uint32(f, 0x00000001)

		write_uint32(f, 0x44414548)
		write_int16(f, h.max_height*scale)
		write_int16(f, 0)
		write_int16(f, 0)

		write_uint32(f, 0x50594c47)
		write_uint32(f, 128)
		cpos_y = 0
		for i in range(128):
			width = h.char_widths[i]*scale
			height = h.max_height*scale
			pos_x = 0
			pos_y = cpos_y
			advance = width
			bearing_x = 0
			bearing_y = 0

			write_uint32(f, i) # code
			write_int16(f, bearing_x);
			write_int16(f, bearing_y);
			write_int16(f, advance);
			write_int16(f, width);
			write_int16(f, height);
			write_int16(f, pos_x);
			write_int16(f, pos_y);

			cpos_y += h.max_height*scale

		# read and paste into one big image
		dst = Image.new("P", (h.max_width*scale, h.max_height*scale * 128))
		attach_palette(dst, pal)

		cpos_y = 0
		for i in range(128):
			name_png = "{}.{:03}.png".format(ff_name, i)
			if os.path.exists(name_png):
				src = Image.open(name_png)

				dst.paste(
					src.resize(
						(src.size[0]*scale, src.size[1]*scale),
						Image.NEAREST
					),
					(0, cpos_y)
				)
			cpos_y += h.max_height*scale

		# write pixel data
		write_uint32(f, 0x414d4141)
		write_int16(f, dst.size[0])
		write_int16(f, dst.size[1])
		for y in range(dst.size[1]):
			for x in range(dst.size[0]):
				r,g,b,a = pal[dst.getpixel((x,y))]
				write_uint8(f, g)

	print(ff_name+'.ftb')


Appendix_1 = """
FTB File Format Specification
-----------------------------
File is in little endian encoding.

uint32_t file_id; // 'FTBF' 0x46425446
uint32_t version; // 1
uint32_t section_id; // 'HEAD' 0x44414548
int16_t height;
int16_t ascender;
int16_t descender;
uint32_t section_id; // 'GLYP' 0x50594c47
uint32_t nglyph;
struct {
	uint32_t code; // less than 256 in version 1
	int16_t bearing_x;
	int16_t bearing_y;
	int16_t advance;
	int16_t width;
	int16_t height;
	int16_t pos_x;
	int16_t pos_y;
} glyphs[nglyph];
uint32_t section_id; // 'AAMA' 0x414d4141
int16_t dim_x;
int16_t dim_y;
uint8_t aamask[dim_y * dim_x]; // row-major order (x y) -> (0 0) (1 0) (2 0) ...
"""
