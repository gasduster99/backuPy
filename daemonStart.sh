#! /bin/bash

#start with backDrive unplugged at boot and then plug it in (before running this script) so it is reconized as sdb instead so sda
sudo e2label /dev/sdb1 backDrive
sudo mount /media/nick/backDrive/

##
#screen -dmS backup0
#screen -S backup0 -X stuff 'cd ~/backups/source/\n'
#screen -S backup0 -X stuff 'python2.7 back.py 0\n'

#
screen -dmS backup
screen -S backup -X stuff 'cd ~/backups/backuPy/\n'
screen -S backup -X stuff 'python3 backMain.py\n'
