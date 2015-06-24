import os
from common import *	

verbose = 0

def read_madsconcat(f, fname):
	
	output_path = '{}.dir'.format(fname)
	lst_name = '{}.lst'.format(fname)
	
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	
	print(output_path)
	print(lst_name)
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
			
	

def write_madsconcat(f, fname):
	
	output_path = '{}.dir'.format(fname)
	lst_file = '{}.lst'.format(fname)
	
	lst = [fn.strip() for fn in open(lst_name, 'r').readlines()]
	
	# idstring	
	f.write(b"MADSCONCAT 1.0\x1A\x00")
	
	# number of files
	numfiles = len(lst)
	write_struct(f, "<H", (numfiles,))
		
	curr_header = f.tell()
	curr_offset = f.tell() + numfiles * struct.calcsize("<II14s")
	
	for fname in lst:
		fpath = os.path.join(input_path, fname)
		length = os.path.getsize(fpath)
		
		# file header
		f.seek(curr_header)
		write_struct(f, "<II14s", (curr_offset,length,fname.encode('ascii')))
		curr_header = f.tell()
		
		# file content
		f.seek(curr_offset)
		f.write(open(fpath,'rb').read())
		curr_offset = f.tell()
	
	
