
from bluetooth import BluetoothSocket, RFCOMM, advertise_service
import time

def start_emulator():
    server_socket = BluetoothSocket(RFCOMM)
    server_socket.bind(("", 1))
    server_socket.listen(1)

    # Set the device name and advertise the service
    advertise_service(server_socket, "RaspberryPiEmulator", service_id="12345678-1234-5678-1234-56789abcdef1")

    print("Emulator waiting for connection...")

    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    data = "Hello, Web Bluetooth!"

    while True:
        client_socket.send(data)
        time.sleep(1)

if __name__ == "__main__":
    start_emulator()