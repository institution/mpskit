mpskit
======

Madspack file format decoder/encoder for Rex Nebular, Dragonsphere, Colonization and other Microprose games. Can run on Linux or Windows (using Cygwin). Designed as a translation/modding tool.


Version 1.8.0

Release Notes
-------------

**1.8.0** - TXR handler; charmap: special handling of "[]" characters (see Notes below)
			
**1.7.1** - fixed bug with transparency handling in SS files

**1.7.0** - partial unpack and pack support for MCC file format from "The Legacy: Realm of Terror", see example

**1.6.0** - lff unpack TMB10 TMB12 TMR10 TMR12 TMR14 HVR08 ("The Legacy: Realm of Terror" font files)

**1.5.0** - charmaps added, see EXAMPLE.md

**1.4.0** - Rex Nebular ART format support added; All png files are now written in indexed mode (see Notes below)

**1.3.0** - MESSAGES.DAT is now unpacked/packed into/from 2 files: MESSAGES.DAT.msg.json and MESSAGES.DAT.id.json. 
If you have modified MESSAGES.DAT.msg.json you will need to pair it up with MESSAGES.DAT.id.json extracted from unmodified MESSAGES.DAT


Installation
------------

1) Install dependencies

* On Debian run `sudo apt-get install python3-pil`
* On Windows install Cygwin (http://cygwin.com/install.html) with following packages (select them during install): wget, python3, python3-imaging, unzip, chere

2) Open terminal (Cygwin terminal on Windows) and run following commands:

```bash

# download
wget -O mpskit.zip https://github.com/institution/mpskit/archive/master.zip
unzip -o mpskit.zip
cd mpskit-master

# install in system path (sudo may be required)
echo "python3 `pwd`/main.py \$*" > /usr/local/bin/mpskit
chmod +x /usr/local/bin/mpskit

# test - should display usage
mpskit

# optional Windows step: add "Open terminal here" option to Windows Explorer
chere -i -t mintty

```


Usage examples
--------------

### General usage ###
	
	cd REX
	
	# unpacking
	mpskit hag unpack GLOBAL.HAG	
	mpskit mdat unpack GLOBAL.HAG.dir/MESSAGES.DAT
	mpskit ss unpack GLOBAL.HAG.dir/*.SS

	# now you can modify generated txt and png files

	# packing
	mpskit ss pack GLOBAL.HAG.dir/GRD1_2.SS
	mpskit mdat pack GLOBAL.HAG.dir/MESSAGES.DAT	
	mpskit hag pack GLOBAL.HAG
	

### Changing AA messages ###

	# unpack
	mpskit hag unpack SECTION9.HAG
	mpskit aa unpack SECTION9.HAG.dir/RM951A.AA

Now in `SECTION9.HAG.dir/RM951A.AA.msg.json`
	
	change this:
	"msg": "\"Here it is, Stone."
	
	to this:
	"msg": "\"Hello, Kitty!"      

	pos_x can be changed to adjust text position on the screen
    "pos_x": 159,


### Modify CNV message ###

	mpskit hag unpack GLOBAL.HAG
	mpskit cnv unpack GLOBAL.HAG.dir/CONV000.CNV
	
	# now modify GLOBAL.HAG.dir/CONV000.CNV.msg.json
	
	mpskit cnv pack GLOBAL.HAG.dir/CONV000.CNV
	mpskit hag pack GLOBAL.HAG


### Adding new letter to font ###

	# for extended example read EXAMPLE.md

	cd GLOBAL.HAG.dir	
	mpskit ff unpack FONTCONV.FF
	cp FONTCONV.FF.099.png FONTCONV.FF.001.png
	
	# edit image of the letter, Gimp works great for this
	# you can modify image width but not height
	#gimp FONTCONV.FF.001.png
		
	mpskit ff pack FONTCONV.FF
	mpskit hag pack ../GLOBAL.HAG
	
### Unpack all supported files ###

	mpskit hag unpack *.HAG
	mpskit ss unpack */*.SS
	mpskit ff unpack */*.FF
	mpskit aa unpack */*.AA
	mpskit txr unpack */*.TXR
	mpskit cnv unpack */*.CNV
	mpskit art unpack */*.ART
	mpskit pik unpack */*.PIK
	
### Create charmap in current directory ###
	
	mpskit charmap create
	
### Legacy: Realm of Terror ###
	
	# unpacking of font files
	mpskit lff unpack T???? HVR08 
	
	mpskit mcc unpack MCC
	mpskit mcc pack MCC
	
	# NOTE 1: MCC colors will be mixed but will work correctly in-game
	# NOTE 2: sprite width and height cannot be modified
	
	
	
	

Supported File Formats
----------------------

|command  |applied to                            |content             |games    |
|---------|--------------------------------------|--------------------|---------|
|hag      |HAG files                             |collection of files |rex      |
|mdat     |MESSAGES.DAT file                     |text                |rex      |
|rdat     |DAT files containing text             |text                |rex      |
|ss       |SS files                              |sprites             |rex,col  |
|aa       |AA files                              |text                |rex      |
|cnv      |CNV files                             |text                |dsp      |
|art      |ART files                             |background image    |rex      |
|ff       |FF files                              |font                |rex      |
|pik      |PIK files                             |background image    |col      |
|lff      |TMB10 TMB12 TMR10 TMR12 TMR14 HVR08   |font                |leg      |
|mcc      |MCC index file                        |sprites             |leg      |
|txr      |TXR files                             |text                |rex      |
|fab      |file containing FAB section           |                    |         |
|madspack |any file which begins with "MADSPACK" |                    |         |

rex = Rex Nebular,
col = Colonization,
dsp = Dragonsphere,
leg = The Legacy: Realm of Terror

Notes
-----

* png files are written in indexed mode with embeded palette ("Colormap" dialog in GIMP)
* changes to embeded palette are ignored by mpskit
* charmap will not be applied to "[]" characters and anything between them

License
-------
AGPLv3 or later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact
-------
Institution, sta256+mpskit@gmail.com

Thanks to
---------
ScummVM Project (http://scummvm.org/)







