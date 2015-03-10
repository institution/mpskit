from common import *
from ctypes import c_uint8, c_uint16, c_uint32, c_int32

verbose = 1




def read_messagesdat(f, g):
	
	# number of entries
	num = read_uint16(f)
	
	if verbose:
		print('read_messagesdat: num={}'.format(num))
	
	curr_header = f.tell()
		
	for _ in range(num):
		# entry header
		f.seek(curr_header)
		sid,offset,length = read_struct(f, "<IIH")
		curr_header = f.tell()
					
		# entry content
		f.seek(offset)
		dest = [b'#'] * length
		read_fab(f, dest)
		
		try:
			entry = ''.join([x.decode('ascii') for x in dest])
			entry = entry.replace('\x00', '|')
		except:
			print(dest)
			raise
			
		# lst entry
		g.write(entry+'\n')


def write_messagesdat(f, g):
	msgs = [x.strip().replace('|', '\x00') for x in g.readlines()]
	
	# num
	num = len(msgs)
	write_uint16(f, num)
	if verbose:
		print('write_messagesdat: num={}'.format(num))
	
	
	curr_header = f.tell()
	curr_offset = f.tell() + num * struct.calcsize("<IIH")
	
	sid = 1
	for data in msgs:
		
		length = len(data)
		
		# head
		f.seek(curr_header)
		write_struct(f, "<IIH", (sid,curr_offset,length))
		curr_header = f.tell()
		
		# body
		f.seek(curr_offset)
		write_fab(f, data.encode('ascii'))
		curr_offset = f.tell()

		
		sid += 1
		
		

'''
return struct.pack("<3sBH15sH1cBBB",
		b'FAB',
		0x0C,
		0xFFFF,
		b'1234567890abcde',
		0xFFFE,
		b'f',
		0x00,
		0x00,
		0x00,
	)
'''

def write_fab(f, data):
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def read_fab(src, dest):
	"""	Decompress fab section
	src -- array
	dest -- array
	return -- length of decoded data
	"""
	
	if not (src.read(3).decode('ascii') == 'FAB'):
		raise Exception('fab_decode: header not found')
	
	shift_val = read_uint8(src)
	if not (10 <= shift_val < 14):
		raise Exception('fab_decode: invalid shift_val: {}'.format(shift_val))
	
	if verbose:
		print("shift_val = {}".format(shift_val))

	
	# uint8s
	copy_len = 0
	copy_ofs_shift = 16 - shift_val
	copy_ofs_mask = 0xFF << (shift_val - 8)
	copy_len_mask = (1 << copy_ofs_shift) - 1


	if verbose:
		print("copy_ofs_shift = {}".format(copy_ofs_shift))
		print("copy_ofs_mask = {}".format(bin(copy_ofs_mask)))
		print("copy_len_mask = {}".format(bin(copy_len_mask)))

	# uint32
	copy_ofs = 0xFFFF0000
	

	_bits_left = 16
	_bit_buffer = read_uint16(src)
		
	j = 0  # dest pos
	
	def get_bit():
		nonlocal _bits_left, _bit_buffer
		
		
		_bits_left -= 1
		if _bits_left == 0:
			
			
			_bit_buffer = (read_uint16(src) << 1) | (_bit_buffer & 1)
			_bits_left = 16
			
			if verbose:
				print('read_bits; i=',src.tell(), bin(_bit_buffer >> 1))
		

		bit = _bit_buffer & 1
		_bit_buffer >>= 1
		return bit
	
	
	while 1:
		# 1 - take next byte literal
		# 00 - copy earlier pattern
		# 01
		if get_bit() == 0:
			if get_bit() == 0:
				# 00
				
				b1 = get_bit()
				b2 = get_bit()
				copy_len = ((b1 << 1) | b2) + 2				
				copy_ofs = read_uint8(src) | 0xFFFFFF00;				
				
				if verbose:
					print("00 {}, {}".format(copy_len, c_int32(copy_ofs).value))
				
			else:
				A = read_uint8(src)
				B = read_uint8(src)
				
				copy_ofs = (((B >> copy_ofs_shift) | copy_ofs_mask) << 8) | A
				copy_len = B & copy_len_mask
				
				if verbose:
					print("01 {}, {}".format(copy_len, c_int32(copy_ofs).value))
								
				if copy_len == 0:
					copy_len = read_uint8(src)
					
					if verbose:
						print("copy_len2 = {}; from {}".format(copy_len, src.tell()-1))
				
					
					if copy_len == 0:
						break
					elif copy_len == 1:
						continue	
					else:
						copy_len += 1
				else:
					copy_len += 2
				
				copy_ofs |= 0xFFFF0000
			
			while copy_len > 0:
				
				dest[j] = dest[j + c_int32(copy_ofs).value]
				
				if verbose:
					print("copy {} from dest {}".format(dest[j + c_int32(copy_ofs).value], j + c_int32(copy_ofs).value))
				
				j += 1
				copy_len -= 1
			
		else:
						
			dest[j] = src.read(1)
			
			if verbose:
				print(dest[j])
			
			
			j += 1
					
	return j

	
	

usage = 'usage: python3 datter.py <"unpack"|"pack"> MESSAGES.DAT messages.dat.txt'
if __name__ == "__main__":
	if len(sys.argv) != 4:
		print(usage)
		sys.exit(1)
		
	cmd = sys.argv[1]
	arg1 = sys.argv[2]
	arg2 = sys.argv[3]
	
	if cmd == 'unpack':
		read_messagesdat(open(arg1, 'rb'), open(arg2, 'w'))
		
	elif cmd == 'pack':
		write_messagesdat(open(arg1, 'wb'), open(arg2, 'r'))
		pass
		
	else:
		print(usage)
		sys.exit(1)
		
		
		
	








