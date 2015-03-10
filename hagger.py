from common import *	

def read_madsconcat(f, output_path):
	with open(os.path.join(output_path, 'lst'), 'w') as lst_file:
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
			with open(os.path.join(output_path,name), 'wb') as out:
				out.write(f.read(length))
			
			# lst entry
			lst_file.write(name+'\n')
	

def write_madsconcat(f, input_path):
	lst = [fn.strip() for fn in open(os.path.join(input_path, 'lst'), 'r').readlines()]
	
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
	
	
usage = 'usage: python3 hagger.py <"unpack"|"pack"> FILE.HAG existing_dir/'
if __name__ == "__main__":
	if len(sys.argv) != 4:
		print(usage)
		sys.exit(1)
		
	cmd = sys.argv[1]
	arg1 = sys.argv[2]
	arg2 = sys.argv[3]
	
	if cmd == 'unpack':
		read_madsconcat(open(arg1, 'rb'), arg2)
	elif cmd == 'pack':
		write_madsconcat(open(arg1, 'wb'), arg2)
	else:
		print(usage)
		sys.exit(1)
		
		
		
	
	
	
	
