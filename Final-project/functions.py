import http.server
import http.client
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
import json
from Seq1 import Seq1

SERVER = 'rest.ensembl.org'

def read_html_file(filename):
    contents = Path(filename).read_text()
    contents = j.Template(contents)
    return contents

def error_json():
    context = {"error": "The value introduced is not valid"}
    contents = json.dumps(context)
    content_type = 'application/json'
    status_code = 200
    return contents, content_type, status_code

def connection(resource, resource_params):
    connection = http.client.HTTPSConnection(SERVER)
    try:
        connection.request("GET", resource + resource_params)
        response = connection.getresponse()
    except ConnectionRefusedError:
        print("ERROR! impossible to connect to the server")
        exit()
    return response

def extract_json(response):
    json_str = response.read().decode("utf-8")
    data = json.loads(json_str)
    return data

def error():
    contents = Path('./html/error.html').read_text()
    status_code = 404
    content_type = 'text/html'
    return contents, content_type, status_code

def exceptions(path, message):
    context = {'path': path, 'error': message}
    contents = read_html_file("./html/error.html").render(context=context)
    status_code = 404
    content_type = 'text/html'
    return contents, content_type, status_code

def get_id(gene):
    resource = "/homology/symbol/human/" + gene
    resource_params = "?content-type=application/json;format=condensed"
    response = connection(resource, resource_params)
    if response.status == 200:
        data = extract_json(response)
        id = (data["data"][0]["id"])
        return id
    else:
        return None

def elif_json(json_format, path, message):
    if json_format:
        contents, content_type, status_code = error_json()
        return contents, content_type, status_code
    else:
        contents, content_type, status_code = exceptions(path, message)
        return contents, content_type, status_code

def elif_json_200(json_format, context, html_file):
    if json_format:
        contents = json.dumps(context)
        content_type = 'application/json'
    else:
        contents = read_html_file(html_file).render(context=context)
        content_type = 'text/html'
    status_code = 200
    return contents, content_type, status_code

def listSpecies(params, json_format, path):
    html_file = "./html/species.html"
    try:
        limit = int(params["limit"][0])
        if limit >= 0:
            resource = "/info/species"
            resource_params = "?content-type=application/json"
            response = connection(resource, resource_params)
            if response.status == 200:
                data = extract_json(response)
                species = data["species"]
                length = len(species)
                species_name = []
                if limit <= int(length):
                    for specie in species[:limit]:
                        species_name.append(specie["display_name"])
                    context = {"number_species": len(species), "limit_species": limit, "species_name": species_name}
                    contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                    return contents, content_type, status_code
                else:
                    contents, content_type, status_code = elif_json(json_format, path, "The value is not valid, proove with a lower number")
                    return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "The value is not valid, introduce a number greater than 0")
            return contents, content_type, status_code
    except (ValueError, KeyError):
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce a valid numeric value")
        return contents, content_type, status_code

def karyotype(params, json_format, path):
    html_file = "./html/karyotype.html"
    try:
        specie = params["specie"][0]
        specie = specie.split()
        if len(specie) == 1:
            specie = specie[0]
            resource = "/info/assembly/" + specie
            resource_params = "?content-type=application/json"
            response = connection(resource, resource_params)
            if response.status == 200:
                data = extract_json(response)
                karyotype = data["karyotype"]
                context = {"specie": specie, "karyotype": karyotype}
                contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                return contents, content_type, status_code
            else:
                contents, content_type, status_code = elif_json(json_format, path, "The key introduced is not valid")
                return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "Please  introduce just the correct name of the specie")
            return contents, content_type, status_code
    except KeyError:
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce valid values")
        return contents, content_type, status_code

def chromosomeLength(params, json_format, path):
    html_file = "./html/chromosome-length.html"
    try:
        specie = params["specie"][0]
        specie = specie.split()
        chromo = int(params["chromo"][0])
        if len(specie) == 1:
            specie = specie[0]
            if chromo >= 0:
                resource = "/info/assembly/" + specie
                resource_params = "?content-type=application/json"
                response = connection(resource, resource_params)
                if response.status == 200:
                    data = extract_json(response)
                    top_level_region = data["top_level_region"]
                    found = False
                    i = 0
                    length = None
                    while not found and i < len(top_level_region):
                        d = top_level_region[i]
                        if d["name"] == str(chromo):
                            found = True
                            length = d["length"]
                        i += 1
                    if found:
                        context = {"length": length, "specie": specie, "chromo": chromo}
                        contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                        return contents, content_type, status_code
                    else:
                        contents, content_type, status_code = elif_json(json_format, path, "The chromosome introduced is not valid")
                        return contents, content_type, status_code
                else:
                    contents, content_type, status_code = elif_json(json_format, path, "The specie introduced is not valid")
                    return contents, content_type, status_code
            else:
                contents, content_type, status_code = elif_json(json_format, path, "The value introduced is not valid, it must be more than 0")
                return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "Please introduce the correct name of the specie")
            return contents, content_type, status_code
    except (ValueError, KeyError):
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce valid values")
        return contents, content_type, status_code

def geneSeq(params, json_format, path):
    html_file = "./html/gene_sequence.html"
    try:
        gene = params["gene"][0]
        gene = gene.split()
        if len(gene) == 1:
            gene = gene[0]
            id = get_id(gene)
            if id:  # if id is not None
                resource = "/sequence/id/" + id
                resource_params = "?content-type=application/json"
                response = connection(resource, resource_params)
                if response.status == 200:
                    data = extract_json(response)
                    bases = data["seq"]
                    context = {"gene": gene, "bases": bases}
                    contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                    return contents, content_type, status_code
            else:
                contents, content_type, status_code = elif_json(json_format, path, "The gene introduced is not valid")
                return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "Please introduce just the correct name of the gene")
            return contents, content_type, status_code
    except KeyError:
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce valid values")
        return contents, content_type, status_code

def geneInfo(params, json_format, path):
    html_file = "./html/gene_information.html"
    try:
        gene = params["gene"][0]
        gene = gene.split()
        if len(gene) == 1:
            gene = gene[0]
            id = get_id(gene)
            if id:  # if id is not None
                resource = "/overlap/id/" + id
                resource_params = "?feature=gene;content-type=application/json"
                response = connection(resource, resource_params)
                if response.status == 200:
                    data = extract_json(response)
                    found = False
                    i = 0
                    start = None
                    end = None
                    length = None
                    chromosome_name = None
                    while not found and i < len(data):
                        if data[i]["id"] == id:
                            found = True
                            start = data[i]["start"]
                            end = data[i]["end"]
                            length = end - start
                            chromosome_name = data[i]["assembly_name"]
                        i += 1
                    if found:
                        context = {"gene": gene, "start": start, "end": end, "length": length,
                                   "chromosome_name": chromosome_name, "id": id}
                        contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                        return contents, content_type, status_code
                    else:
                        contents, content_type, status_code = elif_json(json_format, path, "The chromosome introduced is not valid")
                        return contents, content_type, status_code
            else:
                contents, content_type, status_code = elif_json(json_format, path, "The gene introduced is not valid")
                return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "Please introduce just the correct name of the gene")
            return contents, content_type, status_code
    except KeyError:
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce valid values")
        return contents, content_type, status_code

def geneCalc(params, json_format, path):
    html_file = "./html/gene_calculations.html"
    try:
        gene = params["gene"][0]
        gene = gene.split()
        if len(gene) == 1:
            gene = gene[0]
            id = get_id(gene)
            if id:  # if id is not None
                resource = "/sequence/id/" + id
                resource_params = "?content-type=application/json"
                response = connection(resource, resource_params)
                if response.status == 200:
                    data = extract_json(response)
                    bases = data["seq"]
                    s = Seq1(bases)
                    context = {"gene": gene, "info": s.info(), "length": s.len()}
                    contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                    return contents, content_type, status_code
            else:
                contents, content_type, status_code = elif_json(json_format, path, "The gene introduced is not valid")
                return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "Please introduce just the correct name of the gene")
            return contents, content_type, status_code
    except KeyError:
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce valid values")
        return contents, content_type, status_code

def geneList(params, json_format, path):
    html_file = "./html/gene_list.html"
    try:
        chromo = int(params["chromo"][0])
        end = int(params["end"][0])
        start = int(params["start"][0])
        length = end - start
        if length > 0:
            if chromo > 0:
                resource = f"/overlap/region/human/{chromo}:{start}-{end}"
                resource_params = "?feature=gene;feature=transcript;feature=cds;feature=exon;content-type=application/json"
                response = connection(resource, resource_params)
                if response.status == 200:
                    data = extract_json(response)
                    print(data)
                    name = []
                    for gene in data:
                        if "external_name" in gene:
                            name.append(gene["external_name"])
                    context = {"chromo": chromo, "end": end, "start": start, "name": name, "length": length}
                    contents, content_type, status_code = elif_json_200(json_format, context, html_file)
                    return contents, content_type, status_code
                else:
                    contents, content_type, status_code = exceptions(path, "There is no gene list for these parameters")
                    return contents, content_type, status_code
            else:
                contents, content_type, status_code = elif_json(json_format, path, "The chromosome number must be higher than 0")
                return contents, content_type, status_code
        else:
            contents, content_type, status_code = elif_json(json_format, path, "The length value must be higher than 0")
            return contents, content_type, status_code
    except (KeyError, ValueError):
        contents, content_type, status_code = elif_json(json_format, path, "Please introduce valid values")
        return contents, content_type, status_code








