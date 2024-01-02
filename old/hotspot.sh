#!/bin/bash

# Set hotspot name
hotspot_name="SNESController"

# Log file path
log_file="lognew.txt"  # Replace with the actual path

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
sudo iw wlan0 set type ibss

# Set the IBSS parameters for an open network
sudo iw dev wlan0 ibss join "$hotspot_name" $((2437)) HT20 fixed-freq

# Bring wlan0 back up
sudo ip link set wlan0 up

# Start services
sudo systemctl start dhcpcd
sudo systemctl start wpa_supplicant
