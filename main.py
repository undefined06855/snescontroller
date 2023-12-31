# Import necessary libraries
import bluetooth
import time
import subprocess

subprocess.run(["sudo", "hciconfig", "hci0", "piscan"])

# Set up Bluetooth device information
device_name = "SNESController"
service_uuid = "b032c868-0ffe-4cd9-8345-6b7115173b2f"

# Create Bluetooth socket
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

# Advertise the Bluetooth service
bluetooth.advertise_service(server_socket, device_name,
                            service_id=service_uuid,
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

#print(f"Waiting for connection on {bluetooth.port}")
print("waiting for connection on any port")
try:
    while True:
        # Accept connection from client
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")

        try:
            while True:
                # Send sample data
                data = "Hello, SNESController!"
                client_socket.send(data)
                time.sleep(1)  # adjust delay as needed

        except OSError:
            pass
        finally:
            # Clean up the connection
            client_socket.close()

except KeyboardInterrupt:
    print("Exiting...")
    server_socket.close()
