#!/bin/bash

# this needs to be run as su
if [ "$EUID" -ne 0 ]
  then echo "Needs to be run as root!"
  exit
fi

echo deleting old logs...
rm *.log
echo git pulling...
git pull origin main                                    &> gitpull.log

# comment out the next few lines to enable ssh and disable the controller hotspot

python -u ./web.py                                      &> pythonwebstuff.log

