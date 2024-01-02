#!/bin/bash

# IF YOU EVER NEED TO SET THIS UP AGAIN:


# run this to install hostapd:
# sudo apt-get install hostapd

# then use nano as sudo to set /etc/hostapd/hostapd.conf:
# interface=wlan0
# driver=nl80211
# ssid=SNESController
# hw_mode=g
# vchannel=6
# macaddr_acl=0
# auth_algs=1
# ignore_broadcast_ssid=0
# vwpa=0

# then use nano as sudo to set /etc/dnsmasq.conf:
# interface=wlan0
# dhcp-range=192.168.1.2,192.168.1.10,255.255.255.0,12h

# and it should all be set up!



# IF I EVER NEED TO RUN THIS ON STARTUP

# to get ~/snescontroller/startup.sh to run on startup, edit
# /etc/rc.local using nano as sudo and add the following before the
# exit 0 line:
# sudo -u pi /bin/bash /home/pi/snescontroller/startup.sh
# (assuming pi is the username of the current user)
# then make it executable using sudo chmod +x /etc/rc.local









# Set hotspot name and password
hotspot_name="SNESController"
hotspot_password="snescontroller"

# Log file path
log_file="./FOREST.txt"  # Replace with the actual path

# Redirect all output to the log file
exec &> "$log_file"

# Stop services
sudo systemctl stop dhcpcd
sudo systemctl stop wpa_supplicant

# Bring down wlan0
sudo ip link set wlan0 down

# Unload the wireless driver
sudo rmmod brcmfmac
sudo rmmod brcmutil

# Load the wireless driver with the correct mode
sudo modprobe brcmfmac
sudo modprobe brcmutil
sudo iwconfig wlan0 mode ad-hoc

# Set the IBSS parameters
sudo iwconfig wlan0 essid "$hotspot_name" mode ad-hoc
sudo iwconfig wlan0 key off  # Disable encryption for ad-hoc
sudo iwconfig wlan0 channel 6

# Bring wlan0 back up
sudo ip link set wlan0 up

# Configure IP address for wlan0
sudo ifconfig wlan0 192.168.1.1 netmask 255.255.255.0 up

# Use hostapd to set up the ad-hoc network
sudo hostapd -B /etc/hostapd/hostapd.conf

# Configure DHCP server for wlan0
sudo dnsmasq -C /etc/dnsmasq.conf -d