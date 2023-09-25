import socket

BYTES_TO_READ = 4096

def get(host, port):
    """Send a basic HTTP GET request to the specified host and port, then print the response."""
    
    # Define request headers
    request = b"GET / HTTP/1.1\r\nHost: " + host.encode('utf-8') + b"\r\n\r\n"
    
    # Create a TCP socket. Question 1 AF_INET means that the socket will use IPv4. SOCK_STREAM means that the socket is a TCP socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Establish connection to the host
    s.connect((host, port))
    
    # Send the request
    s.send(request)
    
    # Close the write end to indicate finished sending
    s.shutdown(socket.SHUT_WR)
    
    # Read and print the response
    response = s.recv(BYTES_TO_READ)
    while response:
        print(response)
        response = s.recv(BYTES_TO_READ)
    
    s.close()

# Example usage
get("localhost", 8080)
