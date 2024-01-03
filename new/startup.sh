#!/bin/bash
echo Running...

# make sure to do this before running the rest, else you'd need to actually take
# out the sd card to change anything! I hope this works...
# edit: IT FUCKING DIDNT I THINK I BROKE IT AAAAAAAAAAAAAAAAAARGH
git pull origin main


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
fsudo iwconfig wlan0 essid SNESController mode ad-hoc
sudo iwconfig wlan0 key off  # Disable encryption for ad-hoc
sudo iwconfig wlan0 channel 6

# Bring wlan0 back up
sudo ip link set wlan0 up

# Configure IP address for wlan0
sudo ifconfig wlan0 192.168.1.1 netmask 255.255.255.0 up

# Use hostapd to set up the ad-hoc network
sudo hostapd -B /etc/hostapd/hostapd.conf

# Configure DHCP server for wlan0
sudo dnsmasq -C /etc/dnsmasq.conf -d &

sleep 2

node main.js &
