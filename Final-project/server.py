import http.server
import http.client
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
from urllib.parse import urlparse, parse_qs
import functions

SERVER = 'rest.ensembl.org'
PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)

        json_format = False
        if 'json' in params and params['json'][0] == '1':
            json_format = True

        contents = Path('./html/error.html').read_text()
        content_type = 'text/html'
        status_code = 404
        try:
            if path == "/":
                contents = Path('./html/index.html').read_text()
                status_code = 200
            elif path == "/listSpecies":
                contents, content_type, status_code = functions.listSpecies(params, json_format, path)
            elif path == "/karyotype":
                contents, content_type, status_code = functions.karyotype(params, json_format, path)
            elif path == "/chromosomeLength":
                contents, content_type, status_code = functions.chromosomeLength(params, json_format, path)
            elif path == "/geneSeq":
                contents, content_type, status_code = functions.geneSeq(params, json_format, path)
            elif path == "/geneInfo":
                contents, content_type, status_code = functions.geneInfo(params, json_format, path)
            elif path == "/geneCalc":
                contents, content_type, status_code = functions.geneCalc(params, json_format, path)
            elif path == "/geneList":
                contents, content_type, status_code = functions.geneList(params, json_format, path)
            elif path == "/sequence":
                contents, content_type, status_code = functions.geneList(params, json_format, path)
        except (ConnectionError, KeyError, IndexError, ValueError):
            pass

        contents_bytes = contents.encode()
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()
        self.wfile.write(contents_bytes)
        return

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()
