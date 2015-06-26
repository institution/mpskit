from common import *
from madspack import read_madspack, save_madspack, write_madspack
from PIL import Image
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


def save_ff_header(ff_name, h):
	n = ff_name+'.s00.json'
	open(n, 'w').write(json.dumps(h.as_list(), indent=2))
	print(n)

def read_ff(ff_name):
	pal = [(0,0,0,0),(0,255,0,255),(0,127,0,255),(0,63,0,255)]
	
	parts = read_madspack(ff_name)
	save_madspack(ff_name, parts)
	
	f = parts[0]
	f.seek(0)
	
	h = Record()
	
	h.max_height = read_uint8(f)
	h.max_width = read_uint8(f)

	# glyphs width in pixels
	# glyph height is max_height
	# null has width 0
	h.char_widths = [0] + read_bytes(f, 127)
	read_uint8(f)  # alignment to 128
	
	# space occupied by glyph is 
	# math.ceil((glyph_width * max_height) / 4.0)   # or is is rounded per line ?
	
	
	# offsets inside section
	h.char_offsets = [2 + 128 + 256] + [read_uint16(f) for _ in range(127)]	
	read_uint16(f)  # alignment
	
	assert f.tell() == 2 + 128 + 256
	
	save_ff_header(ff_name, h)	

	# load glyphs	
	for ch in range(1,128):
		
		width = h.char_widths[ch]
		height = h.max_height
		
		if width == 0:
			continue
		
		img = Image.new("RGBA", (width,height))
		
		y = 0
		while y < height:
			x = 0
			while 1:				
				byte = read_uint8(f)
				
				col = pal[(byte & 0b11000000) >> 6]
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break
				
				col = pal[(byte & 0b00110000) >> 4]
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break
				
				col = pal[(byte & 0b00001100) >> 2]
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break
				
				col = pal[(byte & 0b00000011) >> 0]
				img.putpixel((x,y), col)
				x += 1
				if x == width:
					break
					
				
			y += 1

		oname = "{}.s00.{:03}.png".format(ff_name, ch)
		img.save(oname)
		print(oname)

	
