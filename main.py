import sys
from common import Error, External
from hag import read_madsconcat,write_madsconcat
from dat import read_messagesdat,write_messagesdat
from ss import read_ss, write_ss
from fab import read_fab_unrestricted

def call(fmt,cmd,arg1):
	if '/' in arg1:
		raise External("path not allowed as argument; change directory and use file-name")
	
	if cmd not in ['pack','unpack']:
		raise External("invalid command")
	
	if fmt == 'dat':
		
		if cmd == 'unpack':
			read_messagesdat(open(arg1, 'rb'), arg1)
		elif cmd == 'pack':
			write_messagesdat(open(arg1, 'wb'), arg1)
		
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
			write_fab_unrestricted(arg1)			
		else:
			print(usage)
			sys.exit(1)
		
		
	else:
		raise External('invalid format specification')
		
				

usage = '''usage: mpskit <"hag"|"dat"|"ss"|"fab"> <"unpack"|"pack"> <file-name>'''

def main():
	if len(sys.argv) != 4:
		print(usage)
		sys.exit(1)
		
	fmt = sys.argv[1]
	cmd = sys.argv[2]
	arg1 = sys.argv[3]
	
	try:
		call(fmt,cmd,arg1)
	except External as e:
		print(usage)
		print('ERROR', e)
		sys.exit(1)
	
if __name__ == "__main__":
	main()
	
		
		
