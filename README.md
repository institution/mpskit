mpskit
======

Microprose mads engine file format decoder/encoder for Rex Nebular and other games.

Version 0.8

Installation
------------

```bash
# install dependencies
sudo apt-get install python3-pil

# download and unzip 
wget https://github.com/institution/mpskit/archive/master.zip
unzip master.zip

# allow execution
cd mpskit-master
chmod +x mpskit
export PATH="$PATH:`pwd`"

# test - should display usage
mpskit
```

Usage example
-------------

### General usage ###

```bash
# this line will add mpskit to PATH for current session 
# replace "~/mpskit-master" with a path to directory where mpskit is located
export PATH="$PATH:~/mpskit-master"

# copy your REX
cp ~/dosbox/REX . -r

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
cd ..

```

### Changing AA messages ###

```
# unpack
mpskit hag unpack SECTION9.HAG
cd SECTION9.HAG.dir
mpskit aa unpack RM951A.AA
```

Now in RM951A.AA.msg.json change
```json
    [
      "msg",
      "\"Here it is, Stone.\u0000\u00fd'++\b\u0006\u0006\u00fe\u0004*)\u00fe\u0004*\u00fe\u0004\u001a\u0016\u001d\u0004\u0018\u0016\u0017\u0017\u0017\u0019\u0007\u00ff\u00fe\u00fe\u0005\u00fd\u0002\u0006\u000e\t\b\u00fe\u0004)*)\u00fe\u0004"
    ],
```
to
```json
    [
      "msg",
      "\"Hello, Kitty!"      
    ],
```

Back to console
```
# pack again
mpskit aa pack RM951A.AA
cd ..
mpskit hag pack SECTION9.HAG
```

Now when you run REX the intro dialog will be changed!


Limitations
-----------

* While modifying unpacked png files use only colors already existing in the image
* Do not change images dimensions


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
`Institution` <sta256+mpskit at gmail.com>

Thanks to
---------
ScummVM Project (http://scummvm.org/)







