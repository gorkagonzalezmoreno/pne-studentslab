from client0 import client

PRACTICE = 2
EXERCISE = 1

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "localhost" # your IP address
PORT = 8080

# -- Create a client object
c = client(IP, PORT)

# -- Test the ping method
c.ping()
