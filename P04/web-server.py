import socket
import termcolor
from pathlib import Path

IP = "127.0.0.1"
PORT = 8080


def process_client(client_socket):
    request_bytes = client_socket.recv(2048)
    request = request_bytes.decode()
    print("Message FROM CLIENT: ")
    lines = request.splitlines()
    request_line = lines[0]
    print("Request line: ", end="")
    termcolor.cprint(request_line, 'green')

    slices = request_line.split(" ")
    resource = slices[1]
    print(f"Resource: {resource}")

    status_line = "HTTP/1.1 200 OK\n"
    header = status_line
    header += "Content-Type: text/html\n"
    if resource == "/":
        body = Path("html/index.html").read_text()
    elif resource == "/info/A":
        body = Path("html/A.html").read_text()
    elif resource == "/info/C":
        body = Path("html/C.html").read_text()
    elif resource == "/info/G":
        body = Path("html/G.html").read_text()
    elif resource == "/info/T":
        body = Path("html/T.html").read_text()
    else:
        body = Path("html/error.html").read_text()
    header += f"Content-Length: {len(body)}\n"
    response = f"{header}\n{body}"
    response_bytes = response.encode()
    client_socket.send(response_bytes)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

print("SEQ Server configured!")

try:
    while True:
        print("Waiting for clients....")

        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()
except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()