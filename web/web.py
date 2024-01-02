# Python code for hosting a normal server and a websocket server

HOST = "localhost"
WEB_PORT = 80
SOCKET_PORT = 1000


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
