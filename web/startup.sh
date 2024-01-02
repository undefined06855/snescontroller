sudo rm *.log
git pull origin main &> gitpull.log
# comment out the next line to enable ssh and disable the controller hotspot
sudo bash ./create_hotspot.sh &> hotspotcreate.log
sudo python ./web.py &> python.log
