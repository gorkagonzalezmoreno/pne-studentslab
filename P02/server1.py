import socket

# Configure the Server's IP and PORT
PORT = 8080
IP = "localhost" # it depends on the machine the server is running
MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print("Waiting for connections at {IP}:{PORT}")
        (client_socket, client_address) = serversocket.accept() #client_adrees es el ip y port del cliente. el ip es el mismo y el puerto

        # Another connection!e
        number_con += 1

        # Print the conection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, client_address))

        # Read the message from the client, if any
        msg = client_socket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the messag
        message = "Hello from the teacher's server\n"
        send_bytes = str.encode(message)
        # We must write bytes, not a string
        client_socket.send(send_bytes)
        client_socket.close()

except socket.error:
    print("Problems using port {}. Do you have permission?".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()
