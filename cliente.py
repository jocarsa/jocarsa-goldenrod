import socket

# Server Configuration
SERVER_HOST = '192.168.1.210'  # Replace with server's IP if running on different machines
SERVER_PORT = 3000         # Port to connect to

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            # Connect to the server
            client.connect((SERVER_HOST, SERVER_PORT))
            print(f"[CONNECTED] Connected to server at {SERVER_HOST}:{SERVER_PORT}")

            while True:
                # Get user input
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("[DISCONNECTING] Disconnecting from the server.")
                    break

                # Send the message to the server
                client.sendall(message.encode('utf-8'))

                # Wait for the server's response
                response = client.recv(1024)
                if not response:
                    print("[DISCONNECTED] Server closed the connection.")
                    break

                # Decode and print the response
                print(f"Server response: {response.decode('utf-8')}")

        except ConnectionRefusedError:
            print(f"[ERROR] Could not connect to server at {SERVER_HOST}:{SERVER_PORT}. Is the server running?")
        except KeyboardInterrupt:
            print("\n[EXIT] Client terminated by user.")

if __name__ == "__main__":
    start_client()
