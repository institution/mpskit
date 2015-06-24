#!/usr/bin/python3
import sys
from common import Error
from hag import read_madsconcat,write_madsconcat
from dat import read_messagesdat,write_messagesdat
from ss import read_ss, write_ss

def call(fmt,cmd,arg1):
	if cmd not in ['pack','unpack']:
		raise Error("invalid command")
	
	if fmt == 'dat':
		
		if cmd == 'unpack':
			read_messagesdat(open(arg1, 'rb'), arg1)
		elif cmd == 'pack':
			write_messagesdat(open(arg1, 'wb'), arg1)
		
	elif fmt == 'hag':
	
		if cmd == 'unpack':
			read_madsconcat(open(arg1, 'rb'), arg1)
		elif cmd == 'pack':
			write_madsconcat(open(arg1, 'wb'), arg1)
	
	
	elif fmt == 'ss':
		if cmd == 'unpack':
			read_ss(open(arg1, 'rb'), arg1)
		elif cmd == 'pack':
			write_ss(open(arg1, 'wb'), arg1)
		else:
			print(usage)
			sys.exit(1)
		
	else:
		raise Error('invalid format')
		
				

usage = 'usage: python3 mps.py <"hag"|"dat"|"ss"> <"unpack"|"pack"> <file-name>'
if __name__ == "__main__":
	if len(sys.argv) != 4:
		print(usage)
		sys.exit(1)
		
	fmt = sys.argv[1]
	cmd = sys.argv[2]
	arg1 = sys.argv[3]
	
	call(fmt,cmd,arg1)
	
		
		
