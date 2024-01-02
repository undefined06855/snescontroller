sudo rm *.log
git pull origin main            &> gitpull.log
# comment out the next few lines to enable ssh and disable the controller hotspot
sudo bash ./create_hotspot.sh   &> hotspotcreate.log
echo true                       &> conformation.log
sudo python -u ./web.py         &> pythonwebstuff.log
