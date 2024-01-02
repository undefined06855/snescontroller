sudo rm *.log
git pull origin main            &> gitpull.log
# comment out the next few lines to enable ssh and disable the controller hotspot
echo running python...
sudo python -u ./web.py         &> pythonwebstuff.log
sudo bash ./create_hotspot.sh   &> hotspotcreate.log

