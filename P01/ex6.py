from seq1 import Seq1

print("-----| Practice 1, Exercise 6 |------")
sequences = []
s1 = Seq1()
s2 = Seq1("ACTGA")
s3 = Seq1("Invalid sequence")
sequences.append(s1)
sequences.append(s2)
sequences.append(s3)
for i, s in enumerate (sequences):
    print(f"Sequence {i + 1}:  (Length: {s.len()}) {s.bases}")
    print(f"\tBases {s.count()}")