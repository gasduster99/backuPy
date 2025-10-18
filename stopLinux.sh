#!/bin/bash

#Linux
export DISPLAY=:1 
##Mac
#foundDisplay=$(ls -t /private/tmp/com.apple.launchd.*/org.xquartz:0 | head -1)
#export DISPLAY=$foundDisplay

#Linux
nohup vlc -I dummy -q ~/Documents/programs/backuPy/downTone.mp3 &
##Mac
#afplay ~/Documents/programs/backuPy/downTone.mp3

#
xcowsay --image ~/Documents/programs/backuPy/tux.png -t 10 --bubble-at -150,-100 --think Backup Complete



