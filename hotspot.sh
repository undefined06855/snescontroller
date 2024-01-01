#!/bin/bash

# Set hotspot name and password
hotspot_name="SNESController"
hotspot_password="snescontroller"

# Log file path
log_file="./log3.txt"  # Replace with the actual path

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

# Start services
sudo systemctl start dhcpcd
sudo systemctl start wpa_supplicant