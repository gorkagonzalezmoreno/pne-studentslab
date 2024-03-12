from seq1 import Seq1
s = Seq1()
FILENAME = "../Genes/U5.txt"
s.read_fasta(FILENAME)

print("-----| Practice 1, Exercise 9 |------")
print(f"Sequence {s}: (Length: {s.len()}) {s.bases}")
print(f"\tBases: {s.count()}")
print(f"\tRev: {s.reverse()}")
print(f"\tComp: {s.complement()}")




