from client0 import client
from seq1 import Seq1

PRACTICE = 2
EXERCISE = 5
gene = "FRAT1"

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "localhost"
PORT = 8080

c = client(IP, PORT)
print(c)
s = Seq1()
s.read_fasta(gene + ".txt")

print(f"Gene FRAT1: {s}")
msg = f"Sending {gene} gene to the server in fragments of 10 bases..."
response = c.talk(msg)
string = str(s)
n = 0
i = 0
while n < 5:
    f = string[i:i+10]
    print("Fragment:", f)
    msg = f"Fragment {f}"
    response = c.talk(msg)
    n += 1
    i += 10