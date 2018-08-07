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
import sys
from common import Error, warning
import os, sys
import common
from charmap import load_charmap, save_default_charmap
from fail import fail
from hag import read_madsconcat,write_madsconcat
from dat import read_mdat, write_mdat
from rdat import read_rdat, write_rdat
from tdat import read_tdat, write_tdat
from tdat import read_tdat, write_tdat
from ss import read_ss, write_ss
from fab import read_fab_unrestricted
from madspack import read_madspack, save_madspack, load_madspack, write_madspack
from aa import read_aa, write_aa
from ff import read_ff, write_ff, export_ftb
from cnv import read_cnv, write_cnv
from pik import read_pik
from art import read_art, write_art
from lff import read_lff, write_lff
from mcc import read_mcc, write_mcc
from txr import read_txr, write_txr


def get_handler(fmt, cmd, cwd):
	if cmd not in ['pack','unpack']:
		print(usage)
		fail('invalid command; use "pack" or "unpack"')
	
	h = None
		
	if fmt == 'mdat':
		load_charmap(cwd)
		if cmd == 'unpack':
			h = read_mdat
		elif cmd == 'pack':
			h = write_mdat
		
	elif fmt == 'rdat':
		load_charmap(cwd)
		if cmd == 'unpack':
			h = read_rdat
		elif cmd == 'pack':
			h = write_rdat
		
	elif fmt == 'tdat':
		load_charmap(cwd)
		if cmd == 'unpack':
			h = read_tdat
		elif cmd == 'pack':
			h = write_tdat
						
	elif fmt == 'hag':
		if cmd == 'unpack':
			h = read_madsconcat
		elif cmd == 'pack':
			h = write_madsconcat
		
	elif fmt == 'ss':
		if cmd == 'unpack':
			h = read_ss
		elif cmd == 'pack':
			h = write_ss
					
	elif fmt == 'fab':
		if cmd == 'unpack':
			h = read_fab_unrestricted
		elif cmd == 'pack':
			fail("fab compression? what for?")
			# write_fab_unrestricted(arg1)		
		
	elif fmt == 'madspack':
		if cmd == 'unpack':			
			h = lambda arg1: save_madspack(arg1, read_madspack(arg1))
			
		elif cmd == 'pack':
			h = lambda arg1: write_madspack(arg1, load_madspack(arg1))
				
	elif fmt == 'aa':
		load_charmap(cwd)
		if cmd == 'unpack':			
			h = read_aa
			
		elif cmd == 'pack':
			h = write_aa
					
	elif fmt == 'cnv':
		load_charmap(cwd)
		if cmd == 'unpack':
			h = read_cnv
			
		elif cmd == 'pack':
			h = write_cnv
				
	elif fmt == 'ff':
		if cmd == 'unpack':			
			h = read_ff
			
		elif cmd == 'pack':
			h = write_ff

	elif fmt == 'ftb':
		if cmd == 'unpack':			
			fail("ftb unpacking not supported")
			
		elif cmd == 'pack':
			h = export_ftb
							
	elif fmt == 'pik':
		if cmd == 'unpack':			
			h = read_pik
			
		elif cmd == 'pack':
			fail("pik packing not implemented because nobody requested it")
				
	elif fmt == 'art':
		if cmd == 'unpack':			
			h = read_art
			
		elif cmd == 'pack':
			h = write_art
	
	elif fmt == 'lff':
		if cmd == 'unpack':			
			h = read_lff
			
		elif cmd == 'pack':
			h = write_lff
			warning("lff packing not yet implemented")
	
	elif fmt == 'mcc':
		if cmd == 'unpack':			
			h = read_mcc
			
		elif cmd == 'pack':
			h = write_mcc
			
	elif fmt == 'txr':
		load_charmap(cwd)
		if cmd == 'unpack':			
			h = read_txr
			
		elif cmd == 'pack':
			h = write_txr
									
	else:		
		print(usage)	
		fail('invalid format specification')
		
	
	if h is None:
		print(usage)
		sys.exit(1)
		
	return h




def call_handler(handler, path):
	odd = os.getcwd()	
	ndd,arg1 = os.path.split(path)		
	common.g_curr_dir = ndd
	
	if ndd:
		os.chdir(ndd)
		
	try:
		handler(arg1)
	
	finally:
		os.chdir(odd)
		common.g_curr_dir = ''


def call(fmt, cmd, paths):
		
	h = get_handler(fmt, cmd, cwd=os.getcwd())
	
	for path in paths:
		call_handler(h, path)
	

				

usage = '''usage: mpskit <"hag"|"mdat"|"rdat"|"ss"|"aa"|"cnv"|"ff"|"fab"|"madspack"|"pik"|"art"|"lff"|"mcc"|"ftb"|"txr"|"tdat"> <"unpack"|"pack"> [file-name ...] 
'''



def main():
	if len(sys.argv) == 3:
		a,b = sys.argv[1], sys.argv[2]
		if (a,b) == ('charmap', 'create'):
			save_default_charmap(os.getcwd())
			return
						

	if len(sys.argv) < 3:
		print(usage)
		sys.exit(1)
		
	fmt = sys.argv[1]
	cmd = sys.argv[2]
	args = sys.argv[3:]
	
	call(fmt,cmd,args)
	
	
if __name__ == "__main__":
	main()
	
		
		
