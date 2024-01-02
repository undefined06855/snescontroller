# CODE FROM CREATE_HOTSPOT.SH MOVED INTO THE PYTHON FILE
import os
import time

print("--------- PYTHON START")

commands = [
    "sudo systemctl stop dhcpcd",
    "sudo systemctl stop wpa_supplicant",

    # Bring down wlan0
    "sudo ip link set wlan0 down",

    # Unload the wireless driver
    "sudo rmmod brcmfmac",
    "sudo rmmod brcmutil",

    # Load the wireless driver with the correct mode
    "sudo modprobe brcmfmac",
    "sudo modprobe brcmutil",
    "sudo iwconfig wlan0 mode ad-hoc",

    # Set the IBSS parameters
    "sudo iwconfig wlan0 essid \"$hotspot_name\" mode ad-hoc",
    "sudo iwconfig wlan0 key off",  # Disable encryption for ad-hoc
    "sudo iwconfig wlan0 channel 6",

    # Bring wlan0 back up
    "sudo ip link set wlan0 up",

    # Configure IP address for wlan0
    "sudo ifconfig wlan0 192.168.1.1 netmask 255.255.255.0 up",

    # Use hostapd to set up the ad-hoc network
    "sudo hostapd -B /etc/hostapd/hostapd.conf",

    # Configure DHCP server for wlan0
    "sudo dnsmasq -C /etc/dnsmasq.conf -d"
]



for command in commands:
    print("-----------------------------------------------------------------")
    print("executing %s" % command)
    os.system(command)
    print("executed")
    time.sleep(.1)

print("------------------------------ COMMANDS DONE ---")




# Python code for hosting a normal server and a websocket server

HOST = "192.168.1.1"
WEB_PORT = 80
SOCKET_PORT = 1000

print("Setting up server...")

# Import necessary libraries
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from threading import Thread
from inputs import get_gamepad

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Define route for serving files
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Define function for handling WebSocket connections
@socketio.on("connect")
def handle_connect():
    print("WebSocket client connected")

# Define function for handling gamepad events and sending data through WebSocket
def gamepad_listener():
    previous_state = {}  # Store the previous state of buttons

    while True:
        for event in get_gamepad():
            data = {}
            if event.ev_type == "Absolute":
                # dpad movement
                if event.code == "ABS_X":
                    data["direction"] = "left" if event.state == 0 else "center" if event.state == 127 else "right"
                if event.code == "ABS_Y":
                    data["direction"] = "up" if event.state == 0 else "center" if event.state == 127 else "down"

            if event.ev_type == "Key":
                # face buttons
                if event.code == "BTN_THUMB":
                    data["button"] = "A"
                elif event.code == "BTN_THUMB2":
                    data["button"] = "B"
                elif event.code == "BTN_TRIGGER":
                    data["button"] = "X"
                elif event.code == "BTN_TOP":
                    data["button"] = "Y"
                
                # bumpers
                elif event.code == "BTN_TOP2":
                    data["button"] = "L"
                elif event.code == "BTN_PINKIE":
                    data["button"] = "R"

                # start / select
                elif event.code == "BTN_BASE4":
                    data["button"] = "Start"
                elif event.code == "BTN_BASE3":
                    data["button"] = "Select"

            # Check if the button state has changed
            if event.ev_type == "Key" and event.state != previous_state.get(event.code, 0):
                socketio.emit("gamepad_data", data)

            # Update the previous state
            previous_state[event.code] = event.state

# Start the Flask app and WebSocket in separate threads
if __name__ == "__main__":
    server_thread = Thread(target=app.run, kwargs={"host": HOST, "port": WEB_PORT})
    socketio_thread = Thread(target=socketio.run, kwargs={"host": HOST, "port": SOCKET_PORT})

    server_thread.start()
    socketio_thread.start()

    gamepad_listener()  # This will run in the main thread
