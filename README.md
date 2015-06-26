mpskit
======

Installation
------------

```bash
wget https://github.com/institution/mpskit/archive/master.zip
unzip master.zip
cd mpskit-master
chmod +x mpskit
export PATH="$PATH:`pwd`"
```

Usage example
-------------

```bash

# copy your REX
cp ~/dosbox/REX . -r

# unpack
cd REX
python3 mpskit hag unpack GLOBAL.HAG

cd GLOBAL.HAG.dir
python3 mpskit dat unpack MESSAGES.DAT
python3 mpskit ss unpack *.SS

# now you can modify generated txt and png files

# pack
python3 mpskit ss pack GRD1_2.SS
python3 mpskit dat pack MESSAGES.DAT
cd ..

python3 mpskit hag pack GLOBAL.HAG
cd ..

```

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
sta256+mpskit at gmail.com

Thanks to
---------
ScummVM Project (http://scummvm.org/)

