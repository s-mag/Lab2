import socket
from threading import Thread

# Constants for server configuration
BYTES_TO_READ = 4096
HOST = "127.0.0.1"  # This is equivalent to HOST = "localhost"
PORT = 8080

def handle_connection(conn, addr):
    """
    Handle client connection.
    
    Args:
    - conn (socket): Socket object for client.
    - addr (tuple): Address tuple containing IP and port of client.
    """
    with conn:
        print(f"Connected by {addr}")
        
        while True:
            data = conn.recv(BYTES_TO_READ)
            
            # Break the loop if no more data is received from the client
            if not data:
                break
            
            print(f"Data received: {data}")
            
            # Echo the received data back to the client
            conn.sendall(data)

def start_server():
    """
    Start a simple server without threading.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the server to the specified HOST and PORT
        s.bind((HOST, PORT))
        
        # Set the reusability of the socket during linger time
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Start listening for incoming connections
        s.listen(2)
        
        # Accept a connection from a client
        conn, addr = s.accept()
        
        # Handle the connection
        handle_connection(conn, addr)

def start_threaded_server():
    """
    Start a server that uses threading to handle multiple client connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the server to the specified HOST and PORT
        s.bind((HOST, PORT))
        
        # Set the reusability of the socket during linger time
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Start listening for incoming connections
        s.listen(2)
        
        # Continuously accept and handle client connections using threads
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            
            # Start the thread
            thread.start()

# Uncomment to start the desired server
# start_server()
start_threaded_server()
