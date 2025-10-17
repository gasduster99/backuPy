#!/bin/bash

#
export DISPLAY=:1 
##export DISPLAY=/private/tmp/com.apple.launchd.KAxnDWCQtJ/org.xquartz:0
#foundDisplay=$(ls -t /private/tmp/com.apple.launchd.*/org.xquartz:0 | head -1)
#export DISPLAY=$foundDisplay

nohup vlc -I dummy -q ~/Documents/programs/backuPy/upTone.mp3 &
#nohup vlc -I dummy -q ~/Documents/programs/backupSys/upTone.mp3 &
#afplay ~/Documents/programs/backupSys/upTone.mp3

xcowsay --image ~/Documents/programs/backuPy/tux.png -t 10 --bubble-at -150,-100 --think Starting Backup
#xcowsay --image ~/Documents/programs/backupSys/tux.png -t 10 --bubble-at -150,-100 --think Starting Backup



