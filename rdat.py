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
Raw DAT: null-terminated strings, no compression, no madspack

"""
verbose = 0

def read_rdat(name):
	check_ext(name, '.DAT')
		
	r = open(name, 'rb').read()
	xs = r.split(b'\x00')
	
	msgs = [decode_string(x) for x in xs]
	
	on = '{}.rdat.json'.format(name)
	with open(on, 'w') as f:
		json.dump(msgs, f, indent=2)
		
	output(on)
	
def write_rdat(name):
	check_ext(name, '.DAT')
	
	on = '{}.rdat.json'.format(name)
	with open(on, 'r') as f:
		msgs = json.load(f)
	
	xs = [encode_string(m, null_term=True) for m in msgs]
	
	with open(name, 'wb') as f:
		for x in xs:
			f.write(x)
	
	output(name)
	
