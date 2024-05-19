import http.client
import json
from http import HTTPStatus
import functions

SERVER = 'localhost'
PORT = 8080
connection = http.client.HTTPConnection(SERVER, port=PORT)

def url(filename, params):
    endpoint = filename
    parameters = params + '&json=1'
    url = SERVER + ':8080' + endpoint + parameters
    connection = http.client.HTTPConnection(SERVER, port=PORT)
    try:
        connection.request("GET", endpoint + parameters)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()
    response = connection.getresponse()
    json_str = response.read().decode("utf-8")
    data = json.loads(json_str)
    return data

def limit(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        for i in data["species_name"]:
            print(f"{i}")
        print(f"Length introduced: {data['limit_species']}")
        print(f"Length: {data['number_species']}")

def karyotype(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        for i in data["karyotype"]:
            print(f"{i}")

def chromolength(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        print(f"Chromosome length: {data['length']}")

def geneseq(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        print(f"Sequence: {data['bases']}")

def geneinfo(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        print(f"Start: {data['start']}")
        print(f"Length: {data['length']}")
        print(f"Id: {data['id']}")
        print(f"Name: {data['chromosome_name']}")

def genecalc(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        print(f"Sequence: {data['info']}")
        print(f"Length: {data['length']}")

def genelist(data):
    if 'error' in data:
        print(f"ERROR:{data['error']}")
    else:
        print(f"Sequence: {data['name']}")

print("\nList of species")
limit(url('/listSpecies', '?limit=8'))
limit(url('/listSpecies', '?limit=0'))
limit(url('/listSpecies', '?limit=ewgfyu'))
limit(url('/listSpecies', '?limit=500'))
limit(url('/listSpecies', '?limit=-23'))

print("\nKaryotype")
karyotype(url('/karyotype', '?specie=human'))
karyotype(url('/karyotype', '?specie=3652'))
karyotype(url('/karyotype', '?specie=rodrigo'))
karyotype(url('/karyotype', '?specie=e35gaqbd65'))

print("\nChromosomes length")
chromolength(url('/chromosomeLength', '?specie=human&chromo=18'))
chromolength(url('/chromosomeLength', '?specie=rodrigo&chromo=18'))
chromolength(url('/chromosomeLength', '?specie=human&chromo=-21'))
chromolength(url('/chromosomeLength', '?specie=human&chromo=58'))
chromolength(url('/chromosomeLength', '?specie=mouse&chromo=6'))

print("\nGenes Sequence")
geneseq(url('/geneSeq', '?gene=FRAT1'))
geneseq(url('/geneSeq', '?gene=rodrigo'))
geneseq(url('/geneSeq', '?gene=54s98dfde5'))
geneseq(url('/geneSeq', '?gene=69542486'))

print("\nGene info")
geneinfo(url('/geneInfo', '?gene=FRAT1'))
geneinfo(url('/geneInfo', '?gene=patata'))
geneinfo(url('/geneInfo', '?gene=564895448'))
geneinfo(url('/geneInfo', '?gene=dvsv87de4'))

print("\nGene calculations")
genecalc(url('/geneCalc', '?gene=FRAT1'))
genecalc(url('/geneCalc', '?gene=boli'))
genecalc(url('/geneCalc', '?gene=6247861'))
genecalc(url('/geneCalc', '?gene=rf4dd4a2t7'))

print("\nGene list")
genelist(url('/geneList', '?chromo=13&start=22125500&end=22136000'))
genelist(url('/geneList', '?chromo=13&start=22125500&end=2213600'))
genelist(url('/geneList', '?chromo=rodrigo&start=22125500&end=22136000'))
genelist(url('/geneList', '?chromo=13&start=22125500&end='))
genelist(url('/geneList', '?chromo=&start=22125500&end=22136000'))
genelist(url('/geneList', '?chromo=13&start=22125500&end=-22136000'))

