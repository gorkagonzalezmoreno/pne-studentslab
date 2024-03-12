from pathlib import Path


class Seq1:
    BASES = ["A", "C", "T", "G"]
    @staticmethod
    def is_valid(bases):
        ok = True
        i = 0
        while ok and i < len(bases):
            base = bases[i]
            if not base in Seq1.BASES:
                ok = False
            i += 1
        return ok




    def __init__(self, bases=None):
        if bases is not None:
            if Seq1.is_valid(bases):
                self.bases = bases
                print("New sequence created")
            else:
                self.bases = "ERROR"
                print("Invalid seq!")
        else:
            self.bases = "NULL"
            print("NULL seq created!")

    def __str__(self):
        return f"the sequence is {self.bases}"

    def len(self):
        if self.bases == "NULL" or self.bases == "ERROR":
            return 0
        else:
            return len(self.bases)

    def count_base(self, base):
        if self.bases == "NULL" or self.bases == "ERROR":
            return 0
        else:
            total = 0
            for c in self.bases:
                if c == base:
                    total += 1
            return total
            #return self.bases

    def count(self):
        result = {}
        for base in Seq1.BASES:
            result [base] = self.count_base(base)
        return result

    def reverse(self):
        if self.bases == "NULL" or self.bases == "ERROR":
            return self.bases
        else:
            return self.bases[::-1]

    def complement(self):
        if self.bases == "NULL" or self.bases == "EROOR":
            return self.bases
        else:
            rna = ""
            for base in self.bases:
                if base == "A":
                    rna += "T"
                elif base == "C":
                    rna += "G"
                elif base == "G":
                    rna += "C"
                elif base == "T":
                    rna += "A"
            return rna

    def read_fasta(self, filename=None):
        if filename:
            file_contents = Path(filename).read_text()
            index = file_contents.find('\n')
            self.bases = file_contents[index:].replace('\n', '')




    def most_frequent_base(self):
        for i in range(0, len(self.bases)):
            number_A = 0
            number_C = 0
            number_G = 0
            number_T = 0
            max_value = ""
            max_base = ""
            for e in range(0, len(self.bases)):
                if self.bases[e].lower() == "A":
                    number_A += 1
                elif self.bases[e].lower() == "C":
                    number_C += 1
                elif self.bases[e].lower() == "G":
                    number_G += 1
                elif self.bases[e].lower() == "T":
                    number_T += 1
                list_max = [number_A, number_C, number_G, number_T]
                max_value = max(list_max)
            if max_value == int(number_A):
                max_base += "A"
            elif max_value == int(number_C):
                max_base += "C"
            elif max_value == int(number_G):
                max_base += "G"
            elif max_value == int(number_T):
                max_base += "T"
            if self.bases == "NULL":
                return "NULL"
            elif self.bases == "ERROR":
                return "ERROR"
            else:
                return max_base


