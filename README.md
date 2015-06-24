mpskit
======

Installation
------------

```bash
# download and unpack
wget https://github.com/institution/mpskit/archive/master.zip
unzip master.zip
cd mpskit-master
export PATH="$PATH:`pwd`"
chmod +x mpskit.py
```

Usage example
-------------

```bash

# copy your REX
cp ~/dosbox/REX . -r

# unpack
cd REX
python3 mpskit.py hag unpack GLOBAL.HAG

cd GLOBAL.HAG.dir
python3 mpskit.py dat unpack MESSAGES.DAT
python3 mpskit.py ss unpack OB042.SS

# pack
python3 mpskit.py ss pack OB042.SS
python3 mpskit.py dat pack MESSAGES.DAT
cd ..

python3 mpskit.py hag pack GLOBAL.HAG
cd ..


```

License
-------
AGPLv3 or any later, See LICENSE

Contact
-------
sta256+mpskit at gmail.com
