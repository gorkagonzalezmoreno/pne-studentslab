from pathlib import Path


def staticmethod(args):
    pass


class Seq1:
    BASES = ["A", "C", "G", "T"]
    @staticmethod
    def is_valid(bases):
        i = 0
        ok = True
        while ok and i < len(bases):
            base = bases[i]
            if not base in Seq1.BASES:
                ok = False
            i += 1
        return ok
    
    def init(self, bases = None):
        if bases is not None:
            if Seq1.is_valid(bases):
                self.bases = bases
                print("New sequence created")
            else:
                self.bases = "ERROR"
                print("Invalid seq!")
        else:
            self.bases = "NULL"
            print("Null sequence created")

    def __str__(self):
        return f"the sequence is {self.bases}"

    def len(self):
        if self.bases == "ERROR" or self.bases == "NULL":
            return 0
        else:
            return self.len(self.bases)
    def




