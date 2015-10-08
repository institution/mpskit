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
import os
from common import *	

verbose = 0

def read_madsconcat(f, fname):
	check_ext(fname, '.HAG')
	
	output_path = '{}.dir'.format(fname)
	lst_name = '{}.lst'.format(fname)
	
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	
	output(output_path)
	output(lst_name)
	with open(lst_name, 'w') as lst_file:
		# idstring
		read_idstring(f, b"MADSCONCAT 1.0\x1A\x00")
		
		# number of files
		num_files, = read_struct(f, "<H")
		
		curr_header = f.tell()
			
		for _ in range(num_files):
			# file header
			f.seek(curr_header)
			offset,length,name14 = read_struct(f, "<II14s")
			name = get_asciiz(name14)		
			curr_header = f.tell()
						
			# file content
			f.seek(offset)
			oname = os.path.join(output_path,name)
			with open(oname, 'wb') as out:
				out.write(f.read(length))
			
			# lst entry
			lst_file.write(name+'\n')
			
	

def write_madsconcat(fname):
	check_ext(fname, '.HAG')
	
	
	f = open(fname, 'wb')
	
	dir_path = '{}.dir'.format(fname)
	lst_name = '{}.lst'.format(fname)
	
	lst = [fn.strip() for fn in open(lst_name, 'r').readlines()]
	
	# idstring	
	f.write(b"MADSCONCAT 1.0\x1A\x00")
	
	# number of files
	numfiles = len(lst)
	write_struct(f, "<H", (numfiles,))
		
	curr_header = f.tell()
	curr_offset = f.tell() + numfiles * struct.calcsize("<II14s")
	
	for subfname in lst:
		fpath = os.path.join(dir_path, subfname)
		length = os.path.getsize(fpath)
		
		# file header
		f.seek(curr_header)
		write_struct(f, "<II14s", (curr_offset,length,subfname.encode('ascii')))
		curr_header = f.tell()
		
		# file content
		f.seek(curr_offset)
		f.write(open(fpath,'rb').read())
		curr_offset = f.tell()
	
	
	f.close()
	output(fname)
