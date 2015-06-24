mpskit
======

Installation
------------

```bash
# download and unpack
wget -O mpskit.tar.gz http://gitorious.org/var/mpskit/archive-tarball/master
tar xzf mpskit.tar.gz
cd var-mpskit/

```

Usage examples
--------------

```bash
# install
export PATH="$PATH:~/workspace/mpskit"
chmod +x mpskit.py

# copy your REX
cp ~/dosbox/REX . -r

# unpack
cd REX
python3 mpskit.py hag unpack GLOBAL.HAG GLOBAL.HAG.dir

cd GLOBAL.HAG.dir
python3 mpskit.py dat unpack MESSAGES.DAT MESSAGES.DAT.txt
python3 mpskit.py ss unpack OB042.SS OB042.SS.lst

# pack
python3 mpskit.py ss pack OB042.SS OB042.SS.lst
python3 mpskit.py dat pack MESSAGES.DAT MESSAGES.DAT.txt
cd ..

python3 mpskit.py hag pack GLOBAL.HAG GLOBAL.HAG.dir
cd ..


```

License
-------
AGPLv3 or any later, See LICENSE

Contact
-------
sta256+mpskit at gmail.com
