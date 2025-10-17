#!/bin/bash

#
export DISPLAY=:1 
##export DISPLAY=/private/tmp/com.apple.launchd.KAxnDWCQtJ/org.xquartz:0
#foundDisplay=$(ls -t /private/tmp/com.apple.launchd.*/org.xquartz:0 | head -1)
#export DISPLAY=$foundDisplay

nohup vlc -I dummy -q ~/Documents/programs/backuPy/downTone.mp3 &
#nohup vlc -I dummy -q ~/Documents/programs/backupSys/downTone.mp3 &
#vlc -I dummy ~/Documents/programs/backupSys/downTone.mp3 &
#afplay ~/Documents/programs/backupSys/downTone.mp3

xcowsay --image ~/Documents/programs/backuPy/tux.png -t 10 --bubble-at -150,-100 --think Backup Complete
#xcowsay --image ~/Documents/programs/backupSys/tux.png -t 10 --bubble-at -150,-100 --think Backup Complete



