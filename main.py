import os

# Set hotspot name and password
hotspot_name = "SNESController"
hotspot_password = "snescontroller"

# Command to create hotspot
commands = [
    "sudo systemctl stop dhcpcd",
    "sudo ip link set wlan0 down",
    f"sudo iw dev wlan0 ibss join {hotspot_name} {hotspot_password} freq 2437",
    "sudo ip link set wlan0 up",
    "sudo systemctl start dhcpcd"
]

# Execute the command
for command in commands:
    print("Executing: " + command)
    os.system(command)