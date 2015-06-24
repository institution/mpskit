from io import BytesIO
from common import *
from fab import read_fab

def read_madspack(f):
	"""
	f -- input stream
	"""
	magic = f.read(12).decode('ascii')
	assert magic == 'MADSPACK 2.0', magic
	
	
	f.seek(14)
	_count = read_uint16(f)    # num of parts
	
	
	header = io.BytesIO(f.read(0xA0))   # max 16 parts
	header.seek(0)
	
	parts = []
	for i in range(_count):
		hash_ = read_uint16(header)
		size = read_uint32(header)
		compressed_size = read_uint32(header)
		
		if size == compressed_size:
			## no compression on this entry
			data = BytesIO(f.read(size))
			
		else:
			## compressed
			data = read_fab(f, size)
			
		parts.append(data)
		
	return parts
		
	

def write_madspack(f, parts):
	"""
	f -- output stream
	"""
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
		
		f.write(parts[i].read())
		size = f.tell() - parts_pos
		
		parts_pos = f.tell()
		
		# ------------------------
		f.seek(header_pos)
		
		# hash?
		write_uint16(f, 1)
		
		# size
		write_uint32(f, size)
		
		# compressed_size
		write_uint32(f, size)
		
		header_pos = f.tell()
