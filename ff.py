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

pal = [(0,0,0,0),(0,255,0,255),(0,127,0,255),(0,63,0,255)]

def get_col_index(c):
	if c[3] == 0:
		return 0
	if c == (0,255,0,255):
		return 1
	if c == (0,127,0,255):
		return 2
	if c == (0,63,0,255):
		return 3
	print("error: invalid color: {}".format(c))
	
	

def load_ff_header(ff_name):
	return Record.from_list(
		json.load(open("{}.json".format(ff_name)))
	)
	

def save_ff_header(ff_name, h):
	n = "{}.json".format(ff_name)
	open(n, 'w').write(json.dumps(h.as_list(), indent=2))
	output(n)

def write_ff(ff_name):
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
					ind = get_col_index(img.getpixel((x,y)))
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
	if not ff_name.endswith('.FF'):
		error('ff decoder: invalid extension: {}', ff_name)
	
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
	h.char_widths = [0] + [read_uint8(f) for _ in range(127)]
	
	
	
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

		oname = "{}.{:03}.png".format(ff_name, ch)
		img.save(oname)
		output(oname)

	
