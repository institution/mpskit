from common import *
from madspack import read_madspack, save_madspack, write_madspack
"""
AA file format

MADSPACK with 3 sections

Section 0: Header

Section 1: Messages

Section 2: Frames

Section 3: Misc



"""
def read_aa(aa_name):
	assert aa_name.endswith('.AA')
	
	parts = read_madspack(aa_name)
	save_madspack(aa_name, parts)
	
	h = read_aa_header(aa_name)
	save_aa_header(aa_name, h)

	if len(parts) > 1:
		msgs = read_aa_messages(aa_name, h.msg_count)
		save_aa_messages(aa_name, msgs)


def write_aa(aa_name):
	parts = load_madspack(aa_name)
	
	if len(parts) > 1:
		part1 = BytesIO()	
		write_aa_messages(part1, load_aa_messages(aa_name))
		part1.seek(0)
		parts[1] = part1
	
	write_madspack(aa_name, parts)		
	print(aa_name)
	
	



def read_aa_messages(aa_name, msg_count):
	f = open("{}.s01.part".format(aa_name), 'rb')
	
	msgs = []
	for _ in range(msg_count):
		msgs.append(read_aa_message(f))
	
	return msgs
	
def write_aa_messages(f, ms):
	i = 0
	for m in ms:		
		i += write_aa_message(f, m)
	return i
	

def write_aa_message(f, m):
	i = 0
	i += write_sint16(f, m.sound_id)
	assert "\u0000" in m.msg, repr(m.msg)
	i += write_string(f, 64, m.msg)	
	i += write_string(f, 4, m.unk1)	
	i += write_sint16(f, m.pos_x)
	i += write_sint16(f, m.pos_y)
	i += write_uint16(f, m.flags)
	i += write_uint8(f, m.r1)
	i += write_uint8(f, m.g1)
	i += write_uint8(f, m.b1)
	i += write_uint8(f, m.r2)
	i += write_uint8(f, m.g2)
	i += write_uint8(f, m.b2)
	i += write_string(f, 2, m.unk2)
	i += write_string(f, 6, m.unk3)
	i += write_uint16(f, m.start_frame)
	i += write_uint16(f, m.end_frame)
	i += write_string(f, 2, m.unk4)
	return i
	
	

def read_aa_message(f):
	m = Record()	
	m.sound_id = read_sint16(f)
	m.msg = read_string(f, 64)	
	m.unk1 = read_string(f, 4)	
	m.pos_x = read_sint16(f)
	m.pos_y = read_sint16(f)
	m.flags = read_uint16(f)
	m.r1 = read_uint8(f)
	m.g1 = read_uint8(f)
	m.b1 = read_uint8(f)
	m.r2 = read_uint8(f)
	m.g2 = read_uint8(f)
	m.b2 = read_uint8(f)
	m.unk2 = read_string(f, 2)
	m.unk3 = read_string(f, 6)
	m.start_frame = read_uint16(f)
	m.end_frame = read_uint16(f)
	m.unk4 = read_string(f, 2)
	return m
	
	
def save_aa_messages(aa_name, msgs):
	n = aa_name+'.msg.json'
	open(n, 'w').write(
		json.dumps(
			[msg.as_list() for msg in msgs], 
			indent=2
		)
	)
	print(n)

def load_aa_messages(aa_name):
	n = aa_name+'.msg.json'
	xs = json.loads(
		open(n,'r').read()
	)
	msgs = []
	for x in xs:
		msgs.append(Record.from_list(x))
		
	return msgs
	
	
	
	
		


def save_aa_header(aa_name, h):
	n = aa_name+'.s00.json'
	open(n, 'w').write(json.dumps(h.as_list(), indent=2))
	print(n)
		
		


def read_aa_header(aa_name):
	
	f = open2(aa_name+'.s00.part', 'rb')

	h = Header()

	h.sprite_sets_count = read_uint16(f)
	h.misc_entries_count = read_uint16(f)
	h.frame_entries_count = read_uint16(f)
	h.msg_count = read_uint16(f)
	h.load_flags = read_uint16(f)
	h.char_spacing = read_sint16(f)
	h.bg_type = read_uint16(f)
	h.room_number = read_uint16(f)
	h.unk1 = read_string(f,2)
	h.auto_flag = read_uint16(f)
	h.sprites_index = read_uint16(f)
	h.scroll_pos_x = read_sint16(f)
	h.scroll_pos_y = read_sint16(f)
	h.scroll = read_uint32(f)	
	h.unk2 = read_string(f,6)
	
	h.background_file = read_string(f, 13)
	
	h.sprite_set_names = []
	for i in range(50):
		name = read_string(f, 13)		
		if i < h.sprite_sets_count:
			h.sprite_set_names.append(name)
	
	h.sound_name = read_string(f, 13)
	h.unk_name = read_string(f, 13)
	h.dsr_name = read_string(f, 13)
	h.font_resource = read_string(f, 13)

	h.unk3 = read_uint8(f)

	assert f.tell() == 752

	return h
