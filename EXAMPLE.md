### How to add new letter to Rex? ###

	mpskit hag unpack global.hag
	cd global.hag.dir

	mpskit ff unpack FONTMAIN.FF
	cp FONTMAIN.FF.078.png FONTMAIN.FF.001.png

	# FONTMAIN.FF.001.png is your new letter
	# it will be attached to charcode 1
	# you can paint it now
	# changing width is allowed but keep height the same
	# color palette can be accessed in Gimp with "Colormap" dialog
	

	mpskit rdat unpack VOCAB.DAT

	# open VOCAB.DAT.rdat.json
	# find text "fuzzy dice"
	# and replace it with "\u0001uzzy dice"
	# \u0001 is how you enter charcode in json


	mpskit rdat pack VOCAB.DAT
	mpskit ff pack FONTMAIN.FF
	cd ..
	mpskit hag pack global.hag

	# run Rex, start new game, point mouse at fuzzy dice
	# you will see text "Look at fuzzy dice" with f replaced
	# with your new letter
