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
	
