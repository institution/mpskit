from common import *
from madspack import read_madspack, write_madspack
from collections import namedtuple
from PIL import Image, ImageDraw
from fab import read_fab

ext = 'png'

def read_ss(f, ss_name):
	
	"""
	SS file is a MADSPACK file with 4 parts:

	* part 1
		header
			mode -- part3 encoding
				0 -- linemode
				1 -- FAB and linemode
			count -- number of sprites
			size -- size of part3
		
		
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
	verbose = 1
	
	
	parts = read_madspack(f)
	
	
	for i in range(len(parts)):
		oname = '{}.s{:02}.part'.format(ss_name, i)
		print(oname)
		part = parts[i]
		
		open(oname, 'wb').write(part.read())
		part.seek(0)
		
		
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
		
	
	
	pal = read_pallete(parts[2])
	
	sprites = []
	for i, sprite_header in enumerate(sprite_headers):
		sprite = read_sprite(sprite_header, parts[3], pal, mode = ss_header.mode)
		sprites.append(sprite)
		
		# save sprite
		sprite_name = '{}.{:03}'.format(ss_name, i)
		save_sprite(sprite_name, sprite)
	
	return sprites


	
def save_sprite(sprite_name, sprite):
	oname = sprite_name+'.png'
	sprite.save(oname)
	print(oname)




def write_ss(ss_name):
	f = open(ss_name, 'wb')
	
	ss_header = load_ss_header(ss_name)
	
	
	
	
	
	# pallete
	part2 = open('{}.s{:02}.part'.format(ss_name, 2), 'rb')
	
	pal = read_pallete(part2)
	
	# reverse pallete
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
	
	write_madspack(f, parts)
		
	f.close()
	print(ss_name)
	
	
		

class Header: 
	pass
	

def save_sprite_header(sprite_name, h):
	oname = sprite_name + '.json'
	open(oname, 'w').write(
		json.dumps([
			('start_offset', h.start_offset),
			('length', h.length),
			('width_padded', h.width_padded),
			('height_padded', h.height_padded),
			('width', h.width),
			('height', h.height),
		])
	)
	print(oname)
	


def load_sprite_header(sprite_name):
	kvs = json.loads(open(sprite_name + '.json', 'r').read())	
	h = Header()
	for k,v in kvs:
		setattr(h, k, v)
	return h
	

		
def load_ss_header(ss_name):
	kvs = json.loads(open(ss_name + '.json', 'r').read())	
	h = Header()
	for k,v in kvs:
		setattr(h, k, v)
	return h
	

def save_ss_header(ss_name, h):
	oname = ss_name + '.json'
	open(oname, 'w').write(
		json.dumps([
			('mode', h.mode),
			('unk1', h.unk1),
			('type1', h.type1),
			('type2', h.type2),
			('unk2', h.unk2),
			('nsprites', h.nsprites),
			('unk3', h.unk3),
			('data_size', h.data_size),
			
		])
	)
	print(oname)

def read_ss_header(f):
	h = Header()	
	h.mode = read_uint8(f)
	h.unk1 = read_uint8(f)
	h.type1 = read_uint16(f)
	h.type2 = read_uint16(f)
	h.unk2 = read_bytes(f, 32)	
	assert f.tell() == 0x26
	h.nsprites = read_uint16(f)  
	h.unk3 = read_bytes(f, 108)	
	assert f.tell() == 0x94
	h.data_size = read_uint32(f)   # size of last section (part) (unfabed)
	assert f.tell() == 0x98
	return h




def write_ss_header(f, h):
	write_uint8(f, h.mode)
	write_uint8(f, h.unk1)
	write_uint16(f, h.type1)
	write_uint16(f, h.type2)
	write_bytes(f, h.unk2)	
	assert f.tell() == 0x26
	write_uint16(f, h.nsprites) 
	write_bytes(f, h.unk3)	
	assert f.tell() == 0x94
	write_uint32(f, h.data_size)   # size of last section (part) (unfabed)
	assert f.tell() == 0x98
	return f.tell()
	



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
		
	img.save('{}/pal.{}'.format(dname, ext))





	
def write_sprite(head, data, header, img, rpal):
	"""
	head -- headers part
	data -- data part
	header -- original header
	img -- image
	rpal -- reversed pallete	
	return -- size writen to data
	"""
	
	# 1x1 image is used instead of 0x0 image because 0x0 image cannot be represented as png
	if img.size[0] > 1:
		assert header.width == img.size[0]	
	if img.size[1] > 1:
		assert header.height == img.size[1]
	
	# data
	start = data.tell()
	size = 0
	for y in range(header.height):
		
		size += write_uint8(data, 254)     # pixel line mode
		
		for x in range(header.width):
			size += write_uint8(data, 254)     # len pixels
			size += write_uint8(data, 1)     # len = 1
			
			pix = img.getpixel((x,y))
			if pix == (0,0,0,0):
				# transparent background
				size += write_uint8(data, 0xFD)
			else:		
				col = pix[:3]
				ind = rpal[col]
				size += write_uint8(data, ind)
			
		size += write_uint8(data, 255)
			
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
			img = Image.new("RGBA", (1,1))
			img.putpixel((0,0), (0,0,0,0))
			return img
		else:
			raise Error('invalid encoding of 0x0 image while reading SS file')
			

	img = Image.new('RGBA', (ti.width, ti.height), 'black')
	pix = img.load()
	
	if verbose:
		print("sprite size =", ti.width, ti.height)
	
	i = j = 0
	k = 0
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
	

