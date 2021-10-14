from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import SocketServer
import json
#import cgi
import requests
from requests.auth import HTTPDigestAuth

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        #self._set_headers()
        #self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
        #session = requests.Session()
        #session.auth = ("root", "28823097")
        #auth = session.post('http://' + hostname)
        #url = 'http://192.168.1.61/vapix/doorcontrol'
        url = "http://192.168.1.61/axis-cgi/time.cgi"
        #myobj = {'tdc:AccessDoor': '{Token:Axis-accc8ee11415:1630472964.2333198000}'}
        myobj = { 'apiVersion': '1.0', 'context': '123', 'method': 'getDateTimeInfo'}
        x = requests.post( url=url, json = myobj, auth=HTTPDigestAuth('root', '28823097'))
        print("response" + x.text)
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print 'Starting httpd on port %d...' % port
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        