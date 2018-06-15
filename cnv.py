""" Copyright 2015-2017  sta256+mpskit at gmail.com
    
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
from madspack import read_madspack, save_madspack, write_madspack, load_madspack
"""
CNV file format

MADSPACK with 7 sections

Section 0: header
off		l		desc
--------------------
0x0006	2		msg_count
0x0076	4,2?	part5 size



Section 1: 
Section 2: 
Section 3: 
Section 4: offsets
Section 5: messages
Section 6: 


"""
verbose = 0

def read_cnv(cnv_name):
	check_ext(cnv_name, '.CNV')
		
	parts = read_madspack(cnv_name)
	assert len(parts) == 7
	save_madspack(cnv_name, parts)
	
	h = read_cnv_header(cnv_name)	
	save_cnv_header(cnv_name, h)
		
	msgs = read_cnv_messages(cnv_name, h.msg_count)
	save_cnv_messages(cnv_name, msgs)


def write_cnv(cnv_name):
	check_ext(cnv_name, '.CNV')
	
	part0 = open("{}.s00.part".format(cnv_name), 'wb')
	part4 = open("{}.s04.part".format(cnv_name), 'wb')
	part5 = open("{}.s05.part".format(cnv_name), 'wb')
	
	msgs = load_cnv_messages(cnv_name)
	
	h = load_cnv_header(cnv_name)
	
	offset = 0
	for msg in msgs:		
		enc_msg = encode_string(msg, null_term=True)	
		# offset first
		write_uint16(part4, offset)
		
		offset += write_raw(part5, len(enc_msg), enc_msg)
		
	h.msg_count = len(msgs)
	h.part5_size = offset
	
	write_cnv_header(part0, h)
	
	part0.close()
	part4.close()
	part5.close()	
	
	# join to madspack
	parts = load_madspack(cnv_name)
	assert len(parts) == 7
	write_madspack(cnv_name, parts)
	output(cnv_name)
	
	
def read_cnv_header(cnv_name):
	f = open("{}.s00.part".format(cnv_name), 'rb')
	
	h = Record()
	
	f.seek(0x0006)
	h.msg_count = read_uint16(f)
	
	f.seek(0x0076)
	h.part5_size = read_uint16(f)	
	
	f.seek(0)
	h.dump = decode_buffer(f.read())
	
	return h
	
def write_cnv_header(f, h):
	f.seek(0)
	f.write(encode_buffer(h.dump))
	
	f.seek(0x0006)
	write_uint16(f, h.msg_count)
	
	f.seek(0x0076)
	write_uint16(f, h.part5_size)	
	
	
	
	
	



def load_cnv_header(cnv_name):
	with open('{}.json'.format(cnv_name), 'r') as f:
		return Header.from_dict(json.load(f))
		
def save_cnv_header(cnv_name, h):
	n = '{}.json'.format(cnv_name)
	with open(n, 'w') as f:
		json.dump(h.as_dict(), f, indent=2)
	output(n)




def read_cnv_messages(cnv_name, count):
	f = open("{}.s05.part".format(cnv_name), 'rb')
	
	if verbose:
		print("reading cnv messages; msg_count={}".format(count))
	
	msgs = []
	for _ in range(count):
		
		msg = decode_string(read_until(f,0), null_term=True)
		
		msgs.append(msg)
		
	return msgs



	
	
	
	
def save_cnv_messages(cnv_name, msgs):
	n = cnv_name+'.msg.json'
	open(n, 'w').write(
		json.dumps(
			msgs,
			indent=2,
			ensure_ascii=False
		)
	)
	output(n)

def load_cnv_messages(cnv_name):
	n = cnv_name+'.msg.json'
	msgs = json.loads(
		open(n,'r').read()
	)
	return msgs
	
	
