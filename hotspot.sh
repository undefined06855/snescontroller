#!/bin/bash

sudo systemctl stop dhcpcd
sudo systemctl stop wpa_supplicant
sudo ip link set wlan0 down
sudo iw dev wlan0 set type ibss
sudo iw dev wlan0 ibss join SNESController snescontroller freq 2437
sudo ip link set wlan0 up
sudo systemctl start dhcpcd
sudo systemctl start wpa_supplicant