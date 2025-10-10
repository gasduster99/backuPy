A python program that scans the network to progamatically perform periodic backups and archives of registered Unix machines on the LAN. 

You will need to put your hostname and username in the client.list file.

You will also need to set up passwordless ssh from the backup server to the various clients.
	
	passwordless ssh:
                http://www.linuxproblem.org/art_9.html

You will also need to describe the subnet to scan (e.g. 192.168.1) when you initalize the class.

If you need to install xcowsay on a mac you may need the following:
	
	git clone https://github.com/nickg/xcowsay.git	
	cd xcowsay
	./configure
	make
	sudo make install
