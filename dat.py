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
from fab import *



def save_mdat_messages(mdat_name, h):
	oname = "{}.msg.json".format(mdat_name)
	with open(oname, 'w') as f:
		json.dump(h, f, indent=2)
	output(oname)

def load_mdat_messages(mdat_name):
	with open("{}.msg.json".format(mdat_name), 'r') as f:
		return json.load(f)
	


def read_mdat(f, fname, verbose = 0):
	if fname != 'MESSAGES.DAT':
		warning('mdat decoder: only MESSAGES.DAT allowed')
	
	entries = []
	
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
		
		entry = decode_string(dest.read())
		entries.append(entry)
	
	
	save_mdat_messages(fname, entries)


def write_mdat(f, fname, verbose=0):
	if fname != 'MESSAGES.DAT':
		warning('mdat decoder: only MESSAGES.DAT allowed')
	
	messages = load_mdat_messages(fname)
	
	
	
	#
	msgs = [encode_string(s, null_term=True) for s in messages]
	num = len(msgs)
	
	
	
	with open(fname, 'wb') as f:
		write_uint16(f, num)
		if verbose:
			print('write_messagesdat: count={}'.format(num))
			
		curr_header = f.tell()
		curr_offset = f.tell() + num * struct.calcsize("<IIH")
		
		sid = 1
		for data in msgs:
			
			assert data[-1] == 0
			
			length = len(data)
			
			# head
			f.seek(curr_header)
			write_struct(f, "<IIH", (sid,curr_offset,length))
			curr_header = f.tell()
			
			# body
			f.seek(curr_offset)
			write_fab(f, data)
			curr_offset = f.tell()
			
			sid += 1
		
	
	output(fname)	
		

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

	





