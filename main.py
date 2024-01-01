import os

# Set hotspot name and password
hotspot_name = "SNESController"
hotspot_password = "snescontroller"

# Command to create hotspot
commands = [
    "sudo systemctl stop dhcpcd",
    "sudo ip link set wlan0 down",
    "sudo iw dev wlan0 set type ibss",
    "sudo ip link set wlan0 up",
    f"sudo iw dev wlan0 ibss join {hotspot_name} {hotspot_password} freq 2437",
    "sudo systemctl start dhcpcd"
]

# Execute the command
for command in commands:
    print("Executing: " + command)
    os.system(command)