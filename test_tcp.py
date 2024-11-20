import json
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8888  # The port used by the server


def send_data_to_server(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode("utf-8"))
        print("---- Data sent to server:", message)

        # Receive the echoed data from the server
        data = s.recv(1024)
        print("---- Received from server:", data.decode())
        print()


if __name__ == "__main__":
    send_data_to_server("Hello, ASGI Server!")
    send_data_to_server(
        json.dumps(
            {
                "device_id": "51",
                "latitude": 34.0522,
                "longitude": -118.2437,
                "speed": 50.0,
                "timestamp": "2024-11-19T12:05:00Z",
            }
        )
    )
