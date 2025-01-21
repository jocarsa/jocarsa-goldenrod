import socket
import threading

# Server Configuration
HOST = '192.168.1.210'  # Listen on all available network interfaces
PORT = 3000        # Port to listen on

# File to save received messages
MESSAGE_FILE = 'messages.txt'

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        try:
            while True:
                data = conn.recv(1024)  # Receive data from client
                if not data:
                    break  # No more data, client has closed the connection
                message = data.decode('utf-8')
                print(f"[RECEIVED] {addr}: {message}")

                # Save the message to a text file
                with open(MESSAGE_FILE, 'a') as file:
                    file.write(f"{addr}: {message}\n")

                # Prepare and send a response back to the client
                response = f"Server received your message: {message}"
                conn.sendall(response.encode('utf-8'))
        except ConnectionResetError:
            print(f"[DISCONNECTED] {addr} connection was reset.")
    print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Allow reuse of the address
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the address and port
        server.bind((HOST, PORT))
        server.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

        while True:
            # Wait for a new client connection
            conn, addr = server.accept()
            # Handle the client connection in a new thread
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
