from client0 import client
from seq1 import Seq1
PRACTICE = 2
EXERCISE = 6
gene = "FRAT1"

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "localhost"
PORT = 8080
PORT2 = 8081

c = client(IP, PORT)
c2 = client(IP, PORT2)
print(c)
print(c2)
s = Seq1()
s.read_fasta(gene + ".txt")

print(f"Gene FRAT1: {s}")
msg = f"Sending {gene} gene to the server in fragments of 10 bases..."
response = c.talk(msg)
string = str(s)
i = 0
n = 0
while n < 10:
    f = string[i:i+10]
    print("Fragment:", n +1)
    print(f)
    msg = f"Fragment {n+1} {f}"
    if n % 2 == 0:
        response = c.talk(msg)
    else:
        response = c2.talk(msg)
    n += 1
    i += 10