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

Usage
-----

```bash
# prepare
mkdir global-hag

# unpack
python3 hagger.py unpack ~/dosbox/REX/GLOBAL.HAG global-hag/
python3 datter.py unpack global-hag/MESSAGES.DAT messages-dat.txt

# pack
python3 datter.py pack global-hag/MESSAGES.DAT messages-dat.txt
python3 hagger.py pack ~/dosbox/REX/GLOBAL.HAG global-hag/

```

License
-------
GPLv3 or any later

Contact
-------
sta256+mpskit at gmail.com
