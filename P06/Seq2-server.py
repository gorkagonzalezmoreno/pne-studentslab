import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
from Seq1 import Seq1
import os

PORT = 8080
HTML_FOLDER = "html"
seq_list = ["TAACG", "ACTAC", "GAATC", "GATCA", "ATAGG"]
genes = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
operations = ["info", "comp", "rev"]

socketserver.TCPServer.allow_reuse_address = True

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)

        if self.path == "/":
            contents = Path(f"{HTML_FOLDER}/index.html").read_text()
            contents = jinja2.Template(contents)
            context = {'n_sequences': len(seq_list), 'genes': genes}
            contents = contents.render(context=context)
            self.send_response(200)
        elif self.path == "/ping?":
            contents = Path(f"{HTML_FOLDER}/ping.html").read_text()
            self.send_response(200)
        elif self.path.startswith("/get?"):
            try:
                sequence_number = int(params['sequence_number'][0])
                contents = Path(f"{HTML_FOLDER}/get.html").read_text()
                contents = jinja2.Template(contents)
                context = {'number': sequence_number, 'sequence': seq_list[sequence_number]}
                contents = contents.render(context=context)
                self.send_response(200)
            except (KeyError, IndexError, ValueError):
                contents = Path(f"{HTML_FOLDER}/error.html").read_text()
                self.send_response(404)
        elif self.path.startswith("/gene?"):
            try:
                gene_name = params['gene_name'][0]
                contents = Path(f"{HTML_FOLDER}/gene.html").read_text()
                contents = jinja2.Template(contents)
                file_name = os.path.join("Genes", gene_name + ".txt")
                s = Seq1()
                s.read_fasta(file_name)
                context = {'gene': gene_name, 'sequence': str(s)}
                contents = contents.render(context=context)
                self.send_response(200)
            except (KeyError, IndexError, ValueError):
                contents = Path(f"{HTML_FOLDER}/error.html").read_text()
                self.send_response(404)
        elif self.path.startswith("/operation"):
            try:
                bases = params['bases'][0]
                op = params['op'][0]
                contents = Path(f"{HTML_FOLDER}/operation.html").read_text()
                contents = jinja2.Template(contents)
                s = Seq1(bases)
                if op in operations:
                    if op == "info":
                        result = s.info()
                    elif op == "comp":
                        result = s.complement()
                    elif op == "rev":
                        result = s.reverse()
                    context = {'sequence': str(s), 'op': op, 'result': result}
                    contents = contents.render(context=context)
                    self.send_response(200)
                else:
                    contents = Path(f"{HTML_FOLDER}/error.html").read_text()
                    self.send_response(404)
            except (KeyError, IndexError, ValueError):
                contents = Path(f"{HTML_FOLDER}/error.html").read_text()
                self.send_response(404)

        else:
            contents = Path(f"{HTML_FOLDER}/error.html").read_text()
            self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()