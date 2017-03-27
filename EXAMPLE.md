### How to add new letter to Rex? ###

1. Assign letter to Rex charcode through charmap
	
	# enter Rex main directory
	
	# this command will create charmap in current directory if you don't have one already
	mpskit charmap create
	
	# open charmap-mpskit.json and edit it to look like:
	{
	"000": "|",
	"001": "φ"
	}
	
	# I'm using "φ" (Greek small letter fi) as an example
	# you can assign up to 127 letters here
	# end of string mark "|" can be changed or removed as well
	# unassigned letters will default to ASCII encoding

	# now save your file and go to next step
	
2. Assign image of the letter to Rex charcode

	mpskit hag unpack global.hag
	cd global.hag.dir

	mpskit ff unpack FONTMAIN.FF
	cp FONTMAIN.FF.078.png FONTMAIN.FF.001.png

	# FONTMAIN.FF.001.png is your new letter, 001 in filename is Rex charcode
	# it will be attached to charcode 1; charcode must be in 001 to 127 range
	# you can paint it now
	# changing width is allowed but keep height the same
	# color palette can be accessed in Gimp with "Colormap" dialog
	
	
3. Modify some text and see your letter in-game
	
	mpskit rdat unpack VOCAB.DAT

	# open VOCAB.DAT.rdat.json
	# find text "fuzzy dice"
	# and replace it with "φuzzy dice"
	
	# if you didn't assign letter in charmap you can use
	# "\u0001uzzy dice" where \u0001 is 4 digit hexadecimal value of Rex charcode from step 2
	

	mpskit rdat pack VOCAB.DAT
	mpskit ff pack FONTMAIN.FF
	cd ..
	mpskit hag pack global.hag

	# run Rex, start new game, point mouse at fuzzy dice
	# you will see text "Look at fuzzy dice" with f replaced
	# with your new letter so for ex. "Look at φuzzy dice"



Note: all modified text and json files must be saved in utf-8 encoding
