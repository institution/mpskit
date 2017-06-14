# run variou check to verify corectness

from PIL import Image

def test():
	# this image should contain transparent color index
	x = Image.open('EX.HAG.dir/RM901C1.SS.051.png')	
	assert x.info.get('transparency') == 253


test()
