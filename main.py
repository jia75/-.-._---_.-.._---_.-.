from http.server import BaseHTTPRequestHandler, HTTPServer
import random

def getcolorstograde(): # text format "<color1> <color2>" in three digit hex codes
    digs=["0","3","5","7","9","b","d","f"]
    color1=digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]
    color2=digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]
    return color1+" "+color2

def getleaderboard():
    return "No"

def getwinner(data): # takes in "<color1> <color2> <1/2>"
    entries = data.split(" ")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if (not self.path.startswith("/api")):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_file = open("bigahh_html.html")

            html_cont = html_file.read()
            self.wfile.write(html_cont.encode())

            html_file.close() # close html file
        else:
            if (self.path == "/api/get-colors-to-grade"):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                resp = getcolorstograde()

                self.wfile.write(resp.encode())
            elif (self.path == "/api/send-leaderboard"):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                resp = getleaderboard()

                self.wfile.write(resp.encode())
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                resp = "sorry man no api now"

                self.wfile.write(resp.encode())
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)  # raw bytes
        body = body.decode()
        
        if (self.path == "/api/get-colors-to-grade"):
            result()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
            



HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
