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



