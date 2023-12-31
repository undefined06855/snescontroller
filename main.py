import subprocess
from bluetooth import BluetoothSocket, RFCOMM
import time

def set_device_name(new_name):
    subprocess.run(["sudo", "hciconfig", "hci0", "name", new_name])

def start_emulator():
    set_device_name("RaspberryPiEmulator")

    server_socket = BluetoothSocket(RFCOMM)
    server_socket.bind(("", 1))
    server_socket.listen(1)

    print("Emulator waiting for connection...")

    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    data = "Hello, Web Bluetooth!"

    while True:
        client_socket.send(data)
        time.sleep(1)

if __name__ == "__main__":
    start_emulator()