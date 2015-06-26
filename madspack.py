from io import BytesIO
from common import *
from fab import read_fab, write_fab


"""
MADSPACK format

size repeat content          
---------------------------------------------
12          magic           MADSPACK 2.0
2           ykhm            0x1A
2           count (max 16)
10   16     section_header
     count  section


section_header
size repeat content          
---------------------------------------------
2			flags -- bit 0 set => fab compression
4			size -- uncompressed size
4			csize -- compressed size



"""

def save_madspack(madspack_name, parts):
	for i,part in enumerate(parts):
		part.seek(0)			
		n = "{}.s{:02}.part".format(madspack_name, i)
		open(n, 'wb').write(part.read())
		part.seek(0)
		print(n)
			

def read_madspack(madspack_name):
	"""
	f -- input stream
	"""
	
	f = open2(madspack_name, 'rb')
	
	magic = f.read(12).decode('ascii')
	assert magic == 'MADSPACK 2.0', magic
	
	
	f.seek(14)
	_count = read_uint16(f)    # num of parts
	
	
	header = io.BytesIO(f.read(0xA0))   # max 16 parts
	header.seek(0)
	
	parts = []
	for i in range(_count):
		flag = read_uint16(header)
		size = read_uint32(header)
		compressed_size = read_uint32(header)
		
		if (flag & 1) == 0:
			assert compressed_size == size
			## no compression on this entry
			data = BytesIO(f.read(size))
			
		elif (flag & 1) == 1:
			assert compressed_size != size
			## fab compressed
			data = read_fab(f, size)
			
		else:
			raise Error("madspack unknown mode = {}".format(mode))
						
		parts.append(data)
	
	return parts
		
	

def write_madspack(madspack_name, parts):
	"""
	f -- output stream
	"""
	f = open2(madspack_name, 'wb')
	
	write_ascii(f, 'MADSPACK 2.0')
	write_uint16(f, 0x1A)
	
	assert f.tell() == 14
	
	count = len(parts)
	write_uint16(f, count)    # num of parts
	
	header_pos = f.tell()
	parts_pos = header_pos + 0xA0
		
	for i in range(count):
		
		# ------------------------
		f.seek(parts_pos)
		
		# without fab
		f.write(parts[i].read())
		size = f.tell() - parts_pos
		
		parts_pos = f.tell()
		
		# ------------------------
		f.seek(header_pos)
		
		# hash? mode?
		write_uint16(f, 0)    # mode no_fab = 0, fab = 1
		
		# size
		write_uint32(f, size)
		
		# compressed_size
		write_uint32(f, size)
		
		header_pos = f.tell()
