import bluetooth
import subprocess
import time
import uuid


# Enable Bluetooth
subprocess.run(["sudo", "hciconfig", "hci0", "up"])

# Set the device to discoverable mode
subprocess.run(["sudo", "hciconfig", "hci0", "piscan"])


def emulate_bluetooth_device():
    # Set the Bluetooth device name
    device_name = "SNESController"

    # Generate a unique UUID for the service
    service_uuid = str(uuid.uuid4())

    # Create a Bluetooth socket
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("", bluetooth.PORT_ANY))
    server_socket.listen(1)

    # Advertise the service
    bluetooth.advertise_service(server_socket, "SNESControllerService", service_id=service_uuid)

    print(f"Emulating Bluetooth device: {device_name}")

    try:
        while True:
            print("Waiting for connection...")
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address}")

            try:
                while True:
                    # Send data to the connected device
                    data = "Hello, SNES!"
                    client_socket.send(data)

                    time.sleep(1)  # Adjust as needed

            except KeyboardInterrupt:
                pass
            finally:
                client_socket.close()

    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()
        print("Bluetooth emulation stopped.")

if __name__ == "__main__":
    setup_bluetooth()
    emulate_bluetooth_device()