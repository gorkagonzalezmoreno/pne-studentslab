from pathlib import Path
from seq1 import Seq1

print("-----| Practice 1, Exercise 10|------")
s = Seq1()
s.read_fasta("U5.txt")
print("The most frequent is:", s.most_frequent_base())
s1 = Seq1()
s1.read_fasta("ADA.txt")
print("The most frequent is:", s1.most_frequent_base())
s2 = Seq1()
s2.read_fasta("FRAT1.txt")
print("The most frequent is:", s2.most_frequent_base())
s3 = Seq1()
s3.read_fasta("FXN.txt")
print("The most frequent is:", s3.most_frequent_base())

