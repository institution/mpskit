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
TXR: just a text file
"""

verbose = 0

def read_txr(name):
	check_ext(name, '.TXR')
	
	r = open(name, 'rb').read()
	s = decode_string(r)
	
	on = '{}.json'.format(name)
	with open(on, 'w') as f:
		json.dump(s, f, indent=2, ensure_ascii=False)
		
	output(on)
	
def write_txr(name):
	check_ext(name, '.TXR')
	
	on = '{}.json'.format(name)
	with open(on, 'r') as f:
		s = json.load(f)
	
	r = encode_string(s)
	
	with open(name, 'wb') as f:
		f.write(r)
	
	output(name)
	
