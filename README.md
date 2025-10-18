A python program that scans the network to progamatically perform periodic backups and archives of registered Unix machines on the LAN. 

To install, clone this repo in ~/Documents/programs/ on each machine backed up.
	
	cd ~/Documents/programs/
	git clone git@github.com:gasduster99/backuPy.git

You will need to put your hostname and username in the client.list file.

As well as set up passwordless ssh from the backup server to the various clients. 
http://www.linuxproblem.org/art_9.html

In the preamble of backMain.py you will need to describe where backups will reside as well as describe the subnet to scan (e.g. 192.168.1) at the time of initalizing the backup class.

If you need to install xcowsay on a mac you may need the following:
	
	git clone https://github.com/nickg/xcowsay.git	
	cd xcowsay
	./configure
	make
	sudo make install
