#!/bin/bash

# Set hotspot name and password
hotspot_name="SNESController"
hotspot_password="snescontroller"

# Log file path
log_file="./log4.txt"  # Replace with the actual path

# Generate a random MAC address for the BSSID
random_bssid=$(printf '02:%02X:%02X:%02X:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))

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

# Set the IBSS parameters
sudo iw dev wlan0 ibss join "$hotspot_name" $((2437)) HT20 fixed-freq $random_bssid

# Bring wlan0 back up
sudo ip link set wlan0 up

# Start services
sudo systemctl start dhcpcd
sudo systemctl start wpa_supplicant