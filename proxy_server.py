import socket
from threading import Thread

# Constants for server configuration
BYTES_TO_READ = 4096
HOST = "127.0.0.1"  # This is equivalent to HOST = "localhost"
PORT = 8080

def send_request(host, port, request):
    """
    Send a request to a specified host and port and get the response.

    Args:
    - host (str): The target hostname or IP address.
    - port (int): The target port number.
    - request (bytes): The request payload.

    Returns:
    - bytes: The response data received from the host.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # AF_INET: IPv4, SOCK_STREAM: TCP
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR)  # Close the write end, indicating we're done sending

        # Start reading the incoming data in chunks
        data = s.recv(BYTES_TO_READ)
        result = data
        
        # Continue reading while there's incoming data
        while len(data) > 0:
            data = s.recv(BYTES_TO_READ)
            result += data

        return result

def handle_connection(conn, addr):
    """
    Handle the client connection, process the request and send the response.

    Args:
    - conn (socket): Socket object for client.
    - addr (tuple): Address tuple containing IP and port of client.
    """
    with conn:
        print(f"Connected by {addr}")
        request = b''

        while True:
            data = conn.recv(BYTES_TO_READ)
            
            # If no more data is received, consider the request complete
            if not data:
                break
            
            print(f"Data received: {data}")
            request += data

        # Forward the request and fetch the response
        response = send_request("www.google.com", 80, request)
        
        # Send the response back to the client
        conn.sendall(response)

def start_server():
    """
    Start a proxy server that listens for client requests and forwards them.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to the specified HOST and PORT
        s.bind((HOST, PORT))
        
        # Set socket options
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Start listening for incoming connections
        s.listen(2)
        
        # Accept a connection from a client and handle it
        conn, addr = s.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    """
    Start a proxy server with threading to handle multiple client requests.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to the specified HOST and PORT
        s.bind((HOST, PORT))
        
        # Set socket options
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
