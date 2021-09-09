#!/usr/bin/env python

import instance
import sys
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import sys
disp_count = 0

DEFAULT_PORT=8073

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        global disp_count
        self._set_headers()
        if (self.path != "/favicon.ico"):
            print("Handling request",disp_count, self.path)
            disp_count += 1
            obj = instance.get_instance()
            obj.handler(self)
        else:
            print("    +++Skipping favico request")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        try:
           self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        except:
           print("Unexpected error:", sys.exc_info()[0])

def run(server_class=HTTPServer, handler_class=S, port=DEFAULT_PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port:', port,'...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=DEFAULT_PORT)
