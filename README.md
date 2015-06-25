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
python3 mpskit ss unpack OB042.SS

# pack
python3 mpskit ss pack OB042.SS
python3 mpskit dat pack MESSAGES.DAT
cd ..

python3 mpskit hag pack GLOBAL.HAG
cd ..

```

License
-------
AGPLv3 or any later, See LICENSE

Contact
-------
sta256+mpskit at gmail.com
