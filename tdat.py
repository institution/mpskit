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
"""
Text DAT: one long null-terminated string, no compression, no madspack

"""
verbose = 0

def read_tdat(name):
	check_ext(name, '.DAT')
		
	r = open(name, 'rb').read()
	
	if r.count(b'\x00') > 0:
		fail("not tdat file, use rdat instead")
	
	xs = r.split(b"\r\n")
	
	msgs = [decode_string(x) for x in xs]
		
	on = '{}.tdat.json'.format(name)
	with open(on, 'w') as f:
		json.dump(msgs, f, indent=2, ensure_ascii=False)
		
	output(on)
	
def write_tdat(name):
	check_ext(name, '.DAT')
	
	on = '{}.tdat.json'.format(name)
	with open(on, 'r') as f:
		msgs = json.load(f)
	
	r = b"\r\n".join([encode_string(s) for s in msgs])
	
	with open(name, 'wb') as f:
		f.write(r)
	
	output(name)
	
