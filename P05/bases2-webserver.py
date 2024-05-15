import http.server
import socketserver
import termcolor
from pathlib import Path

PORT = 8081

socketserver.TCPServer.allow_reuse_address = True

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/" or self.path == "/index.html":
            contents = Path("index.html").read_text()
            self.send_response(200)
        else:
            try:
                if self.path == "/info/A":
                    contents = Path("info/A.html").read_text()
                elif self.path == "/info/C":
                    contents = Path("info/C.html").read_text()
                elif self.path == "/info/G":
                     contents = Path("info/G.html").read_text()
                elif self.path == "/info/T":
                     contents = Path("info/T.html").read_text()
                else:
                     contents = Path("html/ERROR.html").read_text()

                self.send_response(200)

            except FileNotFoundError:
                contents = Path("ERROR.html").read_text()
                self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return



with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:

    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()