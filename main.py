import os
import time

# Set hotspot name and password
hotspot_name = "SNESController"
hotspot_password = "snescontroller"

# Commands to create hotspot
commands = [
    "sudo systemctl stop dhcpcd",
    "sudo systemctl stop wpa_supplicant",
    "sudo ip link set wlan0 down",
    f"sudo iw dev wlan0 set type ibss",
    f"sudo iw dev wlan0 ibss join {hotspot_name} {hotspot_password} freq 2437",
    "sudo ip link set wlan0 up",
    "sudo systemctl start dhcpcd",
    "sudo systemctl start wpa_supplicant"
]

# Execute the commands
for command in commands:
    print("Executing: " + command)
    os.system(command)
    # Add a small delay between commands
    time.sleep(1)