def seq_ping():
    print("OK")


def seq_read_fasta():
    from pathlib import Path
    FILENAME = "../S04/sequences/U5.txt"
    file_contents = Path(FILENAME).read_text()
    list_contents = file_contents.split("\n")
    list_contents.pop(0)
    list_contents = (''.join(list_contents))
    seq = ""
    for i in range(0, 20):
        seq += list_contents[i]
        i += 1
    print(seq)


def seq_len():
    from pathlib import Path
    list_genes = ["../S04/sequences/U5.txt", "../S04/sequences/ADA.txt", "../S04/sequences/FRAT1.txt",
                  "../S04/sequences/FXN.txt"]
    for i in range(0, 4):
        FILENAME = list_genes[i]
        file_contents = Path(FILENAME).read_text()
        list_contents = file_contents.split("\n")
        list_contents.pop(0)
        list_contents = (''.join(list_contents))
        caracteres = 0
        for line in list_contents:
            caracteres += len(line)
        print("the length of the gene is: ", caracteres)


def seq_count_base():
    from pathlib import Path
    list_genes = ["../S04/sequences/U5.txt", "../S04/sequences/ADA.txt", "../S04/sequences/FRAT1.txt",
                  "../S04/sequences/FXN.txt"]
    for i in range(0, 4):
        count_a = 0
        count_c = 0
        count_g = 0
        count_t = 0
        c = 0
        FILENAME = list_genes[i]
        file_contents = Path(FILENAME).read_text()
        list_contents = file_contents.split("\n")
        list_contents.pop(0)
        list_contents = (''.join(list_contents))
        while c < len(list_contents):
            if list_contents[c] == "A":
                count_a += 1
            elif list_contents[c] == "C":
                count_c += 1
            elif list_contents[c] == "G":
                count_g += 1
            elif list_contents[c] == "T":
                count_t += 1
            c += 1
        print("The number of A is:", count_a)
        print("The number of C is:", count_c)
        print("The number of T is:", count_t)
        print("The number of G is:", count_g)


def seq_count():
    list1 = ["A", "C", "G", "T"]
    from pathlib import Path
    list_genes = ["../S04/sequences/U5.txt", "../S04/sequences/ADA.txt", "../S04/sequences/FRAT1.txt",
                  "../S04/sequences/FXN.txt"]

    for i in range(0, 4):
        count_a = 0
        count_c = 0
        count_g = 0
        count_t = 0
        c = 0
        list_count = []
        FILENAME = list_genes[i]
        file_contents = Path(FILENAME).read_text()
        list_contents = file_contents.split("\n")
        list_contents.pop(0)
        list_contents = (''.join(list_contents))
        while c < len(list_contents):
            if list_contents[c] == "A":
                count_a += 1
            elif list_contents[c] == "C":
                count_c += 1
            elif list_contents[c] == "G":
                count_g += 1
            elif list_contents[c] == "T":
                count_t += 1
            c += 1
        list_count.append(count_a)
        list_count.append(count_c)
        list_count.append(count_g)
        list_count.append(count_t)
        dictt = dict(zip(list1, list_count))
        print(dictt)


def seq_reverse():
    from pathlib import Path
    FILENAME = "../S04/sequences/U5.txt"
    file_contents = Path(FILENAME).read_text()
    list_contents = file_contents.split("\n")
    list_contents.pop(0)
    list_contents = (''.join(list_contents))
    seq = ""
    for i in range(0, 20):
        seq += list_contents[i]
        i += 1
    print("Fragment:", seq)
    print("Reverse:", seq[::-1])

def seq_complement():
    from pathlib import Path
    FILENAME = "../S04/sequences/U5.txt"
    file_contents = Path(FILENAME).read_text()
    list_contents = file_contents.split("\n")
    list_contents.pop(0)
    list_contents = (''.join(list_contents))
    seq = ""
    for i in range(0, 20):
        seq += list_contents[i]
        i += 1
    rna = ""
    for character in seq:
        if character == "A":
            rna += "U"
        elif character == "C":
            rna += "G"
        elif character == "G":
            rna += "C"
        elif character == "T":
            rna += "A"
    print("Gene U5:")
    print("Frag:", seq)
    print("Comp:", rna)



def seq_process_gene():
    import operator
    list1 = ["A", "C", "G", "T"]
    from pathlib import Path
    list_genes = ["../S04/sequences/U5.txt", "../S04/sequences/ADA.txt", "../S04/sequences/FRAT1.txt",
                  "../S04/sequences/FXN.txt"]
    for i in range(0, 4):
        count_a = 0
        count_c = 0
        count_g = 0
        count_t = 0
        c = 0
        list_count = []
        FILENAME = list_genes[i]
        file_contents = Path(FILENAME).read_text()
        list_contents = file_contents.split("\n")
        list_contents.pop(0)
        list_contents = (''.join(list_contents))
        while c < len(list_contents):
            if list_contents[c] == "A":
                count_a += 1
            elif list_contents[c] == "C":
                count_c += 1
            elif list_contents[c] == "T":
                count_t += 1
            elif list_contents[c] == "G":
                count_g += 1
            c += 1
        list_count.append(count_a)
        list_count.append(count_c)
        list_count.append(count_t)
        list_count.append(count_g)
        dictt = dict(zip(list1, list_count))
        m = max(dictt.items(), key=operator.itemgetter(1))
        print("Most frequent Base:", m[0])