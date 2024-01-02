# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

LOCAL = True

hostName = "localhost"
serverPort = 80





#############################################################################

if LOCAL:
    from time import sleep

indexhtml = open("index.html", "r").read()

class SNEServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # the current url is at self.path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(indexhtml, "utf-8"))


if __name__ == "__main__":        
    server = HTTPServer((hostName, serverPort), SNEServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    # there won't be a chance to input a KeyboardInterrupt or anything, 
    # so this will just keep serving forever until the power cuts.
    # the only reason this is here is for debugging
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    # in debugging, it should auto refresh
    
    while LOCAL:
        indexhtml = open("index.html", "r").read()
        sleep(0.1)
