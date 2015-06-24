from common import *
from madspack import read_madspack, write_madspack
from collections import namedtuple
from PIL import Image, ImageDraw

def read_ss(f, fname):
	
	"""
	SS file is a MADSPACK file with 4 parts:

	* part 1
		header, not sure about content
		
	* part 2
		is composed of tile_headers, there can be many tiles in one file 
		ntiles = len(part2) / 0x00000010

	* part 3
		palette
		
	* part 4	
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
	verbose = 0
	
	
	parts = read_madspack(f)
	
	
	for i in range(len(parts)):
		oname = '{}.part.{:01}'.format(fname, i)
		print(oname)
		part = parts[i]
		
		open(oname, 'wb').write(part.read())
		part.seek(0)
		
		
	h = read_ss_header(parts[0])
	
	f1 = parts[1]
	shead = []
	for _ in range(h.ntiles):
		shead.append(read_sprite_header(f1))
	
	pal = read_pallete(parts[2])
	
	if verbose:
		print("ntiles=",h.ntiles)
	
	imgs = []
	f3 = parts[3]
	for i in range(h.ntiles):
		if verbose:
			print("reading tile i=", i)
			
		img = read_ss_tile(shead[i], f3, pal)
		oname = '{}.{:03}.png'.format(fname, i)
		img.save(oname)
		print(oname)
		
		imgs.append(img)
		
	return imgs



def write_ss(fname):
	f = open(fname, 'wb')
	
	
	parts = [None,None,None,None]
	
	# header
	parts[0] = open('{}.part.{:01}'.format(fname, 0), 'rb')
	
	# pallete
	parts[2] = open('{}.part.{:01}'.format(fname, 2), 'rb')
	
	hh = read_ss_header(parts[0])
	pal = read_pallete(parts[2])
	
	rpal = {}
	for i,col in enumerate(pal):
		rpal[col] = i
	
		
	parts[1] = BytesIO()
	parts[3] = BytesIO()
		
	for i in range(hh.ntiles):		
		iname = '{}.{:03}.png'.format(fname, i)
		img = Image.open(iname)
		write_ss_tile(parts[1], parts[3], img, rpal)
		
	
	
	for part in parts:
		part.seek(0)
	
	write_madspack(f, parts)
		
	f.close()
	print(fname)
	
	
		
		
	
	

	
	
class Header: 
	pass

	

def read_ss_header(f):
	h = Header()
	
	f.seek(0x00000026)
	h.ntiles = read_uint16(f)   
	
	f.seek(152)
	
	assert f.tell() == 152	
	return h
	


def write_sprite_header(f, h):	
	write_uint32(f, h.start_offset)
	write_uint32(f, h.length)
	write_uint16(f, h.width_padded)
	write_uint16(f, h.height_padded)
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


def vga_color_trans(x):
	return int((x * 255) / 63)

def read_pallete(f):
	"""
		
	uint16 ncolors
	repeat ncolors {
		uint8 red6
		uint8 green6
		uint8 blue6
		uint8 ind
		uint8 u2
		uint8 flags
	}
		
	"""
	
	ncolors = read_uint16(f)

	pal = []

	for _ in range(ncolors):
		rr,gg,bb,ind,u2,flags = reads(f, '6b')
		r,g,b = map(vga_color_trans, [rr,gg,bb])

		assert ind == -1
		pal.append((r,g,b))
		
	assert len(pal) == ncolors
		
	return pal
	

def export_pallete(pal, trg):
	img = Image.new('P', (16,16), 0)
	img.putpalette(reduce(operator.add, pal))
	
	d = ImageDraw.ImageDraw(img)
	d.setfill(1)
	for j in range(16):
		for i in range(16):
			d.setink(j*16 + i)			
			d.rectangle((i, j, i+1, j+1))
		
	img.save('{}/pal.png'.format(dname))

	
def write_ss_tile(hpart, dpart, img, rpal):
	"""
	hpart -- headers part
	dpart -- data part
	img -- image
	rpal -- reversed pallete	
	"""
	
	# data
	data = dpart
	start = data.tell()
	for y in range(img.size[1]):
		
		write_uint8(data, 254)     # pixel line mode
		
		for x in range(img.size[0]):
			write_uint8(data, 254)     # len pixels
			write_uint8(data, 1)     # len = 1
			
			pix = img.getpixel((x,y))
			if pix == (0,0,0,0):
				# transparent background
				write_uint8(data, 0xFD)
			else:		
				col = pix[:3]
				ind = rpal[col]
				write_uint8(data, ind)
			
		write_uint8(data, 255)
			
	write_uint8(data, 252)
		
		
	# header
	h = Header()
	h.width_padded = img.size[0]
	h.height_padded = img.size[1]
	h.width = img.size[0]
	h.height = img.size[1]
	h.start_offset = start
	h.length = data.tell() - start
	
	write_sprite_header(hpart, h)	
	
				



	
def read_ss_tile(ti, rdata, pal, verbose=0):
	"""
	ti -- sprite header
	rdata -- file-like object
	pal -- array of (R,G,B)
	"""
	
	data = rdata.read()
	rdata.seek(0)
	
	img = Image.new('RGBA', (ti.width, ti.height), 'black')
	pix = img.load()
	
	if verbose:
		print("sprite size =", ti.width, ti.height)
	
	i = j = 0
	k = ti.start_offset
	bg = 0xFD
	
	def write_ind(ci, l=1):
		if ci == bg:
			
			c = (0,0,0,0)
			#c = pal[ci] + (0,)
		else:
			c = pal[ci] + (255,)
			
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
	
	lm = read()
	
	if verbose:
		print('lm=',lm)
		
	while 1:   #j < ti.height:  #k < ti.length:
		
		# line mode
		if lm == 255:
			# fill with bg color to the end of this line
			write_ind(bg, ti.width - i)
			nextline()
			lm = read()
			
		elif lm == 252:
			# end of image
			break
			
		else:
			x = read()
			if x == 255:
				write_ind(bg, ti.width - i)			
				nextline()
				lm = read()			
		
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
	

