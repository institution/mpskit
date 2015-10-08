import sys
from common import Error, External, warning, InvalidMadspackVersion
from hag import read_madsconcat,write_madsconcat
from dat import read_mdat, write_mdat
from rdat import read_rdat, write_rdat
from ss import read_ss, write_ss
from fab import read_fab_unrestricted
from madspack import read_madspack, save_madspack, load_madspack, write_madspack
from aa import read_aa, write_aa
from ff import read_ff, write_ff
from cnv import read_cnv, write_cnv
import os, sys
import common

def call(fmt,cmd,path):
	
	odd = os.getcwd()
	
	ndd,arg1 = os.path.split(path)
	
	
	common.g_curr_dir = ndd
	
	if ndd:
		os.chdir(ndd)
		
	try:
		
		if cmd not in ['pack','unpack']:
			print('invalid command; use "pack" or "unpack"')
			sys.exit(1)
		
		
		if fmt == 'mdat':
			
			if cmd == 'unpack':
				read_mdat(open(arg1, 'rb'), arg1)
			elif cmd == 'pack':
				write_mdat(open(arg1, 'wb'), arg1)
		
		elif fmt == 'rdat':
			if cmd == 'unpack':
				read_rdat(arg1)
			elif cmd == 'pack':
				write_rdat(arg1)
							
		elif fmt == 'hag':
		
			if cmd == 'unpack':
				read_madsconcat(open(arg1, 'rb'), arg1)
			elif cmd == 'pack':
				write_madsconcat(arg1)
		
		
		elif fmt == 'ss':
			if cmd == 'unpack':
				read_ss(open(arg1, 'rb'), arg1)
			elif cmd == 'pack':
				write_ss(arg1)
			else:
				print(usage)
				sys.exit(1)
				
		elif fmt == 'fab':
			if cmd == 'unpack':
				read_fab_unrestricted(arg1)			
			elif cmd == 'pack':
				print("fab compression? what for?")
				# write_fab_unrestricted(arg1)		
			else:
				print(usage)
				sys.exit(1)
			
		elif fmt == 'madspack':
			if cmd == 'unpack':			
				save_madspack(arg1, read_madspack(open(arg1, 'rb')))
				
			elif cmd == 'pack':
				write_madspack(arg1, load_madspack(arg1))
							
			else:
				print(usage)
				sys.exit(1)
		
		elif fmt == 'aa':
			if cmd == 'unpack':			
				read_aa(arg1)
				
			elif cmd == 'pack':
				write_aa(arg1)
							
			else:
				print(usage)
				sys.exit(1)
			
		
		elif fmt == 'cnv':
			if cmd == 'unpack':			
				read_cnv(arg1)
				
			elif cmd == 'pack':
				write_cnv(arg1)
							
			else:
				print(usage)
				sys.exit(1)
				
				
		elif fmt == 'ff':
			if cmd == 'unpack':			
				read_ff(arg1)
				
			elif cmd == 'pack':
				write_ff(arg1)
							
			else:
				print(usage)
				sys.exit(1)
			
		else:
			
			raise External('invalid format specification')
			
			
	
	except InvalidMadspackVersion as e:
		warning(*e.args)
		
	
	finally:
		os.chdir(odd)
		common.g_curr_dir = ''
		
				

usage = '''usage: mpskit <"hag"|"mdat"|"rdat"|"ss"|"aa"|"cnv"|"ff"|"fab"|"madspack"> <"unpack"|"pack"> <file-name> [file-name ...] 
'''


def main():
	if len(sys.argv) < 3:
		print(usage)
		sys.exit(1)
		
	fmt = sys.argv[1]
	cmd = sys.argv[2]
	args = sys.argv[3:]
	
	try:
		for arg in args:
			call(fmt,cmd,arg)
	except External as e:
		print(usage)
		print('ERROR', e)
		sys.exit(1)
	
if __name__ == "__main__":
	main()
	
		
		
