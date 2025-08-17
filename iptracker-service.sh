#!/bin/bash
# setup the python env
# make sure we are in the correct directory
cd /home/pi/Alligitor/IPTracker

#generate a file name for screen
logFilename="screen-"$(date +"%Y-%m-%d_%H-%M-%S").log
echo $logFilename

/usr/bin/screen -S IPTracker -d -L -Logfile /tmp/$logFilename -m /usr/bin/python3 iptracker.py -o 

