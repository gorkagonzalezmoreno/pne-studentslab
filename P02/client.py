import socket

# SERVER IP, PORT
SERVER_PORT = 8080
SERVER_IP = "localhost" # it depends on the machine the server is running

# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish the connection to the Server (IP, PORT)
client_socket.connect((IP, PORT))

# Send data. No strings can be sent, only bytes
# It necesary to encode the string into bytes
client_socket.send(str.encode("HELLO FROM THE CLIENT!!! "))

# Receive data from the server
msg = client_socket.recv(2048).decode("utf-8")
print("MESSAGE FROM THE SERVER:\n")
print(msg)

# Closing the socket
client_socket.close()

