import socket

# Constant for buffer size when reading data
BYTES_TO_READ = 4096

def get(host, port):
    """
    Send a GET request to a specified host and port.
    
    Args:
    - host (str): The target hostname or IP address.
    - port (int): The target port number.
    
    Returns:
    - bytes: The response data received from the host.
    """
    # Construct the GET request payload
    request = b"GET / HTTP/1.1\r\nHost: " + host.encode('utf-8') + b"\r\n\r\n"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # AF_INET: IPv4, SOCK_STREAM: TCP
        # Connect to the specified host and port
        s.connect((host, port))
        
        # Send the GET request
        s.send(request)
        
        # Close the write end of the socket to indicate we've finished sending
        s.shutdown(socket.SHUT_WR)

        # Start reading the incoming data in chunks
        chunk = s.recv(BYTES_TO_READ)
        result = chunk
        
        # Continue reading while there's incoming data
        while len(chunk) > 0:
            chunk = s.recv(BYTES_TO_READ)
            result += chunk

        return result

# Uncomment to send a GET request to a specific host and port
# print(get("www.google.com", 80))
print(get("localhost", 8080))  # Or use "127.0.0.1"
