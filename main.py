import os

# Set hotspot name and password
hotspot_name = "SNESController"
hotspot_password = "snescontroller"

# Command to create hotspot
command = (
    f"sudo systemctl stop dhcpcd;"
    f"sudo ip link set wlan0 down;"
    f"sudo iw dev wlan0 set type ibss;"
    f"sudo ip link set wlan0 up;"
    f"sudo iw dev wlan0 ibss join {hotspot_name} {hotspot_password} freq 2437;"
    f"sudo systemctl start dhcpcd;"
)

# Execute the command
os.system(command)