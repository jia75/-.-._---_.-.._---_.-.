from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import csv
import socket
import json

# CONFIG
maxChange = 10

datafile = open("data.csv")
cols = []
count = 0
reader = csv.reader(datafile)
for row in reader:
    cols.append(row)
    count += 1
datafile.close()

leaderboard = []
for row in cols:
    leaderboard.append(row[0])

def getindexfromcolor(color):
    antidigs = {"0" : 0,"6":1,"a":2,"f":3}
    return antidigs[color[0]]*16+antidigs[color[1]]*4+antidigs[color[2]]

leaderboard = sorted(leaderboard, key=lambda a: -float(cols[getindexfromcolor(a)][1]))


def logi(x):
    return 1.0/(1+2**(-float(x)))

def getcolorstograde(): # text format "<color1> <color2>" in three digit hex codes
    digs=["0","6","a","f"]
    color1=digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]
    color2=digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]+digs[random.randint(0,len(digs)-1)]
    return color1+" "+color2

def getleaderboard():
    out = ""
    for color in leaderboard:
        out += color
    return out

def updatefile():
    o = open("data.csv", "w", newline="")
    writer = csv.writer(o)
    writer.writerows(cols)
    o.close()

def getwinner(data): # takes in "<color1> <color2> <1/2>"
    global leaderboard
    entries = data.split(" ")
    if (len(entries) < 3):
        # data that was sent has an error
        return

    coloneind = getindexfromcolor(entries[0])
    coltwoind = getindexfromcolor(entries[1])
    if entries[2] == "1":
        diff = logi(float(cols[coloneind][1])-float(cols[coltwoind][1]))*maxChange
        cols[coloneind][1] = str(float(cols[coloneind][1]) + diff)
        cols[coltwoind][1] = str(float(cols[coltwoind][1]) - diff)
    elif entries[2] == "2":
        diff = logi(-float(cols[coloneind][1])+float(cols[coltwoind][1]))*maxChange
        cols[coloneind][1] = str(float(cols[coloneind][1]) - diff)
        cols[coltwoind][1] = str(float(cols[coltwoind][1]) + diff)

    leaderboard = sorted(leaderboard, key=lambda a: -float(cols[getindexfromcolor(a)][1]))
    updatefile()

class Handler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if (self.path.startswith("/api")):
            if (self.path == "/api/get-colors-to-grade"):
                self.send_response(200)
                self.send_cors_headers()
                self.send_header("Content-type", "application/json")
                self.end_headers()

                color1, color2 = getcolorstograde().split()
                resp = json.dumps({"color1": color1, "color2": color2})
                self.wfile.write(resp.encode())
            elif (self.path == "/api/send-leaderboard"):
                self.send_response(200)
                self.send_cors_headers()
                self.send_header("Content-type", "application/json")
                self.end_headers()

                resp = json.dumps({"leaderboard": leaderboard})
                self.wfile.write(resp.encode())
            else:
                self.send_response(404)
                self.send_cors_headers()
                self.send_header("Content-type", "application/json")
                self.end_headers()

                resp = json.dumps({"error": "API endpoint not found"})
                self.wfile.write(resp.encode())
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)  # raw bytes
        body = body.decode()
        
        if (self.path == "/api/say-result"):
            getwinner(body)
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.send_cors_headers()
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "API endpoint not found"}).encode())


print(f"Server running at http://localhost:2086/ and http://<ip address>:2086/")
HTTPServer(("0.0.0.0", 2086), Handler).serve_forever()
