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
verbose = 0

def load_madspack(madspack_name):
	parts = []
	i = 0
	while i < 16:
		n = "{}.s{:02}.part".format(madspack_name, i)
		if not os.path.exists(n):
			if verbose:
				print('load madspack: file not found:', n)
			break
		parts.append(open(n, 'rb'))
		i += 1
	
	if i == 0:
		print('ERROR: no parts to load')
		sys.exit(2)
		
	return parts
	

def save_madspack(madspack_name, parts):
	for i,part in enumerate(parts):
		part.seek(0)			
		n = "{}.s{:02}.part".format(madspack_name, i)
		open(n, 'wb').write(part.read())
		part.seek(0)
		output(n)
			

def read_madspack(madspack_name):
	"""
	f -- input stream
	"""
	
	f = open2(madspack_name, 'rb')
	
	magic = f.read(12).decode('ascii')
	if magic != 'MADSPACK 2.0':
		raise InvalidMadspackVersion(
			"invalid madspack version; expected=MADSPACK 2.0; got={}; file={}", magic, madspack_name
		)
		
	
	
	
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
			if compressed_size == size:
				warning("madspack decoder: flag indicate fab compression but csize equals usize in: {}", madspack_name)
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
		parts[i].seek(0)
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
	
	output(madspack_name)
