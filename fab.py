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
from ctypes import c_uint8, c_uint16, c_uint32, c_int32

def write_fab(f, data, verbose = 0):
	""" Compress data to FAB sequence
	f -- file object (output)
	data -- bytes array	
	"""

	assert type(data) == bytes
	
	if verbose:
		print('write_fab ----->',data)
	
	# FAB & shift_val
	write_struct(f, '<3sB', (b'FAB', 0x0C))
	
	bits = ''.join(['1'] * len(data) + ['0111', '1111', '1111', '1111'])
		
	i = 0
	
	write_uint16(f,
		int(bits[0:16], 2)
	)
	
	bnext = 0
	
	
	if verbose:
		print('bits =', bits)

	
	def set_bit():
		nonlocal bnext
		
		b = bits[bnext]
		
		bnext += 1
		if not (bnext % 16):			
			chunk = ''.join(reversed(bits[bnext:bnext+16]))
			
			write_uint16(f, int(chunk, 2))
			
			
			if verbose:
				print('write bits =', chunk)
				
			
			
		#if verbose:
		#	print("b =",b)

		return int(b)
	
	
	while 1:
		# 1 - take next byte literal
		# 00 - copy earlier pattern
		# 01
		if set_bit() == 0:
			if set_bit() == 0:
				# not implemented
				assert 0
				
			else:
				# write end sequence				
				write_uint8(f, 0x00)
				write_uint8(f, 0x00)
								
				write_uint8(f, 0x00)
				break
				
		else:
			if verbose:
				print(chr(data[i]))
	
			
			write_uint8(f, data[i])
			i += 1
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def read_fab_unrestricted(fab_name):
	f = open(fab_name, 'rb')
	
	i = 0
	while 1:
		d = read_fab(f)
		d.seek(0)
		oname = '{}.f{:03}.part'.format(fab_name,i)
		open(oname, 'wb').write(d.read())
		output(oname)
		i += 1
		
	
	
	
	
	
from copy import copy
	
def fmt_bits(x_, i_):
	x = copy(x_)
	i = copy(i_)
	
	rs = []
	while i > 0:
		if x & 1:
			rs.append('1')
		else:
			rs.append('0')
		x >>= 1
		i -= 1	
	return "".join(reversed(rs))
	
	

def read_fab(src, length=None, verbose = 0):
	"""	Decompress fab section
	src -- file object
	length -- uncompressed length, only for asserts
	return -- uncompressed data as file object
	"""
	
	dest = io.BytesIO()
	
	start = src.tell()
	
	if not (src.read(3).decode('ascii') == 'FAB'):
		raise Error('fab_decode: header not found')
		
	if verbose:
		print()
		print("FAB decompression start")
	
	shift_val = read_uint8(src)
	if not (10 <= shift_val < 14):
		raise Error('fab_decode: invalid shift_val: {}'.format(shift_val))
	
	#if verbose:
	#	print("READ shift_val = {}".format(shift_val))

	
	# uint8s
	copy_len = 0
	copy_adr_shift = 16 - shift_val
	copy_adr_fill = 0xFF << (shift_val - 8)     # nie maska to jest do wypelniania przed konwersja na negative
	copy_len_mask = (1 << copy_adr_shift) - 1

	# ALL entries in Rex Nebular MESSAGES.DAT look like this:
	# copy_adr_shift = 4
	# copy_adr_fill = 0b11110000
	# copy_len_mask = 0b00001111

	if verbose:
		print("copy_adr_shift = {}".format(copy_adr_shift))
		print("copy_adr_fill = {}".format(fmt_bits(copy_adr_fill, 8)))
		print("copy_len_mask = {}".format(fmt_bits(copy_len_mask, 8)))

	# uint32
	copy_adr = 0xFFFF0000
	

	_bits_left = 16
	_bit_buffer = read_uint16(src)
	
	def bb():
		nonlocal _bits_left, _bit_buffer
		x = _bit_buffer
		i = _bits_left
		return fmt_bits(x,i) + "[{}]".format(i)
		
	
	
	if verbose:
		print("bit_buffer = ", bb())
		
	j = 0  # dest pos
	
	
	# degug only
	cs_bytes = 2
	cs_bits = 0
	
	def get_bit():
		nonlocal _bits_left, _bit_buffer
		nonlocal cs_bytes, cs_bits
		
		
		_bits_left -= 1
		if _bits_left == 0:
			
			
				
			_bit_buffer = (read_uint16(src) << 1) | (_bit_buffer & 1)
			_bits_left = 16
			
			cs_bytes += 2
			
			if verbose:
				print("read from {}; bit_buffer = {}".format(src.tell()-2 - start, bb()))
	
			
			#if verbose:
			#	print('read_bits; i=',src.tell(), bin(_bit_buffer >> 1))
		

		bit = _bit_buffer & 1
		_bit_buffer >>= 1
		
		cs_bits += 1
		
		if verbose:
			print("bb = {}".format(bb()))
			
		return bit
	
	
	while 1:
		# 1 - take next byte literal
		# 00 - copy earlier pattern
		# 01
		if get_bit() == 0:
			if get_bit() == 0:
				# 00, bit, bit, byte
				
				b1 = get_bit()
				b2 = get_bit()
				
				# use 2 bits for copy_len
				# copy_len in range [2,5]
				copy_len = ((b1 << 1) | b2) + 2				
				
				# read negative num in range [255 -> -1, 0 -> -256]
				raw_copy_adr = read_uint8(src)
				copy_adr = raw_copy_adr | 0xFFFFFF00;  
				
				#[0,1,2,3] + 2
				#b1,b2 + 
				
				
				if verbose:
					print("00 copy {} from {}".format(copy_len, c_int32(copy_adr).value))
				
			else:
				# 01, byte A, byte B
				
				A = read_uint8(src)
				B = read_uint8(src)
				
				if verbose:
					print("A =",fmt_bits(A,8))
					print("B =",fmt_bits(B,8))
				
				
				copy_adr = (((B >> copy_adr_shift) | copy_adr_fill) << 8) | A				
				copy_adr |= 0xFFFF0000
				
				# use [3 to 7] (usually 4) bits for copy_len
				copy_len = B & copy_len_mask
				
								
				if copy_len == 0:
				
					# use 8 bits for copy len
					copy_len = read_uint8(src)
					
					if verbose:
						print("copy_len2 = {}; from {}".format(copy_len, src.tell()-1))
				
					
					if copy_len == 0:
						# HALT
						break
						
					elif copy_len == 1:
						# NOP
						continue
						
					else:
						copy_len += 1
						
				else:
					copy_len += 2
								
				
				if verbose:
					print("01 copy {} from {}".format(copy_len, c_int32(copy_adr).value))
				
			
			while copy_len > 0:
	
				dest.seek(j + c_int32(copy_adr).value)
				v = dest.read(1)
				dest.seek(j)
				dest.write(v)
				if verbose:
					print("{:5}: copying  {}".format(j, v))
				
				j += 1
				copy_len -= 1
			
		else:
			
			v = src.read(1)
			dest.seek(j)	
			dest.write(v)
			if verbose:
				print("{:5}: write    {}".format(j, v))
				
			j += 1
		
				
	
	if verbose:
		jj = j
		xs = []
		dest.seek(0)
		while jj > 0:
			xs.append(dest.read(1))
			jj -= 1
		print("OUTPUT = ", b''.join(xs))
			
		print("cs_bytes, cs_bits = ", cs_bytes, cs_bits)
	
	
	if length is not None:	
		assert length == j, (length, j)
	
	
	
	dest.seek(0)
	return dest

	
	

			

			
		
class FAB:

	def __init__(self, shift_val):
		self.copy_adr_shift = 16 - shift_val
			
	def encode_cmd00_xyA(self, copy_len, copy_adr):
		"""
		>>> FAB(12).encode_cmd00_xyA(3, -3)
		(0, 1, 253)
		"""


		assert 2 <= copy_len <= 5 and -255 <= copy_adr <= -1

		# copy_len b1,b2
		q = copy_len - 2
		q,b2 = divmod(q, 2)
		q,b1 = divmod(q, 2)
		
		#print("{} encoded as {}{}".format(copy_len - 2, b1, b2))
		
		# A = neg copy_adr
		A = 256 + copy_adr 
		
		return b1, b2, A



	def encode_cmd01_AB(self, copy_len, copy_adr):
		"""
		>>> f = FAB(12)
		>>> A,B = f.encode_cmd01_AB(6, -1)
		>>> assert A == 0b11111111 and B == 0b11110100
		"""
		assert 3 <= copy_len <= 17 and -(2**12 - 1) <= copy_adr <= -1

		

		neg_copy_adr = (2**12) + copy_adr 
				
		# 4 low bits of B
		B = copy_len - 2
		
		# 4 high bits of B := 4 high bits of neg_copy_adr
		B |= ((neg_copy_adr & 0xFF00) >> (8 - self.copy_adr_shift))
		
		# 8 low bits of neg_copy_adr
		A = neg_copy_adr & 0x00FF

		return A,B
		
		
		
	def encode_cmd01_ABC(self, copy_len, copy_adr):
		"""
		>>> f = FAB(12)
		>>> A,B,C = f.encode_cmd01_ABC(23, -58)
		>>> assert A == 0b11000110 and B == 0b11110000 and C == 0b00010110		
		
		>>> A,B,C = f.encode_cmd01_AB(2, -281)
		>>> print(bin(A),bin(B),bin(C))
		"""
		assert 2 <= copy_len <= 256 and -(2**12 - 1) <= copy_adr <= -1
		
		neg_copy_adr = (2**12) + copy_adr 
		
		# 4 low bits of B - zero indicating copy_len is writen as a separate byte
		B = 0
		
		# 4 high bits of B := 4 high bits of neg_copy_adr
		B |= ((neg_copy_adr & 0xFF00) >> (8 - self.copy_adr_shift))
		
		# 8 low bits of neg_copy_adr
		A = neg_copy_adr & 0x00FF

		C = copy_len - 1

		return A,B,C
		

def write_fab_optimal(f, data, verbose = 0):
	""" Compress data to FAB sequence
	f -- file object (output)
	data -- bytes array	
	
	>>> f = io.BytesIO()
	>>> write_fab_optimal(f, b"abcabc123")
	>>> _ = f.seek(0)
	>>> print(f.read())
	b'FAB\\x0c\\xc7\\x0babc\\xfd123\\x00\\x00\\x00'
	
	>>> f = io.BytesIO()
	>>> write_fab_optimal(f, b'[title29][sentence]\\x00')
	>>> _ = f.seek(0)
	>>> print(f.read())
	b'FAB\\x0c\\xff?[title29][sent\\xbc\\x00\\xfdce]\\x00\\x00\\x00\\x00'
	"""
	
	
	shift_val = 12
	
	fw = FAB(shift_val)
	
	# write 'F' 'A' 'B' shift_val
	write_struct(f, '<3sB', (b'FAB', shift_val))
		
	
	# control sequence current current position (ptr uint16)
	cs = f.tell()
	write_uint16(f, 0)
	
	# data sequence current position (ptr uint8)
	ds = f.tell()
	
	bit_buffer = 0
	bit_length = 0
	
	def write_bit(b):
		nonlocal bit_buffer, bit_length, cs, ds
		
		bit_buffer |= (b << bit_length)
		bit_length += 1
				
		if bit_length == 16:
			f.seek(cs)
			write_uint16(f,bit_buffer)
					
			f.seek(ds)
			write_uint16(f,0)
			cs = ds
			ds += 2
			
			bit_buffer = 0
			bit_length = 0
		
		
	def write_byte(b):
		nonlocal ds
		f.seek(ds)
		write_uint8(f,b)
		ds += 1
		
	
	# possible commands
	# 1 A -- write A
	# 00xy A -- copy 'xy from 'A                           for copy_len in [2,5], rel_adr in [0,-255]
	# 01 A B -- copy 'copy_len from 'copy_adr              for copy_len in [3,17], rel_adr in [0,-(2^12 + 1)]
	# 01 A B [copy_len == 0] C -- copy_len = C             for copy_len in [3,256], rel_adr in [0,-(2^12 + 1)]
	# 01 A B [copy_len == 0] C [copy_len == 0] -- HALT
	# 01 A B [copy_len == 0] C [copy_len == 1] -- NOP
	
	# 4 commands
	
	def cmd_write(b):
		write_bit(1)
		write_byte(b)
	
	def cmd_copy(copy_len, copy_adr):
		assert 2 <= copy_len
		assert copy_adr <= -1
		
		if 2 <= copy_len <= 5 and -255 <= copy_adr <= -1:
			
			b1,b2,A = fw.encode_cmd00_xyA(copy_len, copy_adr)
			
			write_bit(0)
			write_bit(0)
			write_bit(b1)
			write_bit(b2)
			write_byte(A)
			
		elif 3 <= copy_len <= 17 and (-2**12 - 1) <= copy_adr:
		
			A,B = fw.encode_cmd01_AB(copy_len, copy_adr)
			
			write_bit(0)
			write_bit(1)
			write_byte(A)
			write_byte(B)
		
		
		elif 2 <= copy_len <= 256 and (-2**12 - 1) <= copy_adr:
			
			A,B,C = fw.encode_cmd01_ABC(copy_len, copy_adr)
		
			write_bit(0)
			write_bit(1)
			write_byte(A)
			write_byte(B)
			write_byte(C)
	
		else:
			fail("invalid copy_len and copy_adr combination")
	
	
	def cmd_halt():
		write_bit(0)
		write_bit(1)
		write_byte(0)
		write_byte(0)
		write_byte(0)
		
	def cmd_nop():
		write_bit(0)
		write_bit(1)
		write_byte(0)
		write_byte(0)
		write_byte(1)
	
	
	

	i = 0
	while i < len(data):
		max_k = 1
		max_j = -1
		for j in range(max(0, i - 2**16 + 1),i):
			k = 0
			while j + k < i + k and i + k < len(data) and data[j + k] == data[i + k]:
				k += 1
			
			if k > max_k:
				max_k = k
				max_j = j
		
		
		
		if max_k >=2:
			if verbose:
				print(i, "copy {} from {}".format(max_k, max_j - i))
			cmd_copy(max_k, max_j - i)
			i += max_k
			
		else:
			if verbose:
				print(i, "write", chr(TEST[i]))
			cmd_write(data[i])
			i += 1

	cmd_halt()
	
	loc = f.tell()
	
	# flush bit_buffer
	if bit_length > 0:
		f.seek(cs)
		write_uint16(f,bit_buffer)
		
	
	loc = max(loc, f.tell())	
	
	f.seek(loc)
	return
	
	
	
	


TEST = b'[title29][sentence]\x00O.K.  You grab the slip and put it on.\x00You throw the bra on for kicks, and wrap the\x00boa around your neck.  You then skip\x00out into the street where you dance\x00for hours.  And then again, maybe not.\x00\x00'
#TEST = b'[title29][sentence]\x00'
TEST = b'[title21][sentence]\x00They have been rocks for a long time.  They\x00probably will continue to be rocks for a long time.\x00'

TEST = b"[title32][sentence]|You take a moment to look through your|possessions.  Suddenly you realize that|the [noun1] [noun1:is:are] not among them.  How could|you have forgotten to bring [noun1:it:them], you fool?|If you don't HAVE the [noun1], you can|hardly throw [noun1:it:them] at the [noun2], can you?|"

       



def test():
	i = 0
	while i < len(TEST):
		max_k = 1
		max_j = -1
		for j in range(max(0, i - 2**16 + 1),i):
			k = 0
			while j + k < i + k and i + k < len(TEST) and TEST[j + k] == TEST[i + k]:
				k += 1
			
			if k > max_k:
				max_k = k
				max_j = j
		
		
		
		if max_k >=2:
			print(i, TEST[i], "copy {} from {}".format(max_k, max_j - i))
			i += max_k
		else:
			print(i, TEST[i])
			i += 1
			
		
if __name__ == "__main__":
	
	
	f = io.BytesIO()
	write_fab_optimal(f, TEST, verbose=1)
	f.seek(0)
	
	print(f.read())
	f.seek(0)
	out = read_fab(f, length = len(TEST), verbose=1)
	print(out)
	assert out == TEST
	
	
	

