from common import *
from fab import *





def read_messagesdat(f, fname, verbose = 0):
	
	assert fname == 'MESSAGES.DAT'
	
	oname = '{}.txt'.format(fname)
	g = open(oname, 'w')
	print(oname)
	
	
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
		
		dest = read_fab(f, length)
		
		try:
			entry = ''.join([x.decode('ascii') for x in dest])
			entry = entry.replace('\x00', '|')
		except:
			print(dest)
			raise
			
		
			
		# lst entry
		g.write(entry+'\n')


def write_messagesdat(f, fname):
	assert fname == 'MESSAGES.DAT'
	
	uname = '{}.txt'.format(fname)
	g = open(uname, 'r')
	print(fname)
	
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

	





