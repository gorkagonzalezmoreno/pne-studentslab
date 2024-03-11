from client0 import client
from seq1 import Seq1
GENES = ['U5', 'FRAT1', 'ADA']
PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "localhost" # your IP address
PORT = 8080

# -- Create a client object
c = client(IP, PORT)

# -- Test the ping method
print(c)
for gene in GENES:
    s = Seq1()
    s.read_fasta(gene + ".txt")
    msg = f"Sending {gene} Gene to server..."
    print(f"To server: {msg}")
    response = c.talk(msg)
    print("From Server:\n\n")
    print(response)
    print(f"To Server: {s}")
    response = c.talk(str(s))
    print("From Server:\n\n")
    print(response)
...
