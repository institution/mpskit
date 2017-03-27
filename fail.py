import sys

def fail(fmt, *args):
	print('ERROR: ' + fmt.format(*args))
	sys.exit(1)

def info(fmt, *args):
	print('INFO: ' + fmt.format(*args))
	
def warning(fmt, *args):
	print('WARNING: ' + fmt.format(*args))
	
def printf(fmt, *args):
	print(fmt.format(*args))
	
