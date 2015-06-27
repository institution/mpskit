mpskit
======

Microprose madspack file format decoder/encoder for Rex Nebular and other games.

Version 0.9.1

Installation
------------

```bash
# install dependencies
sudo apt-get install python3-pil

# download
wget https://github.com/institution/mpskit/archive/master.zip
unzip master.zip
cd mpskit-master
chmod +x mpskit

# install in system path (optional)
sudo ln -s `pwd`/mpskit /usr/local/bin/mpskit

# test - should display usage
mpskit
```

Usage examples
--------------

### General usage ###

	# unpacking
	cd REX
	mpskit hag unpack GLOBAL.HAG

	cd GLOBAL.HAG.dir
	mpskit dat unpack MESSAGES.DAT
	mpskit ss unpack *.SS

	# now you can modify generated txt and png files

	# packing
	mpskit ss pack GRD1_2.SS
	mpskit dat pack MESSAGES.DAT
	cd ..

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

Back to console

	# pack again
	mpskit aa pack SECTION9.HAG.dir/RM951A.AA
	mpskit hag pack SECTION9.HAG


Now when you run REX the intro dialog will be changed!


### Adding new letter to font ###


	cd GLOBAL.HAG.dir
	mpskit ff unpack FONTCONV.FF
	cp FONTCONV.FF.099.png FONTCONV.FF.001.png
	
	# edit your new letter but do not insert new colors to the image
	# modifying image width is ok
	gimp FONTCONV.FF.001.png
		
	mpskit ff pack FONTCONV.FF
	mpskit hag pack ../GLOBAL.HAG
	



Limitations
-----------

* While modifying unpacked png files use only colors already existing in the image

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
Institution, sta256+mpskit at gmail.com

Thanks to
---------
ScummVM Project (http://scummvm.org/)







