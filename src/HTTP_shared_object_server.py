#!/usr/bin/env python
# a minimal http server

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class Server(BaseHTTPRequestHandler):
    def _set_shared_object(self, shared):
        self.shared = shared

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

    
    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._json())

    def _json(self):
        '''Generate json string of shared object'''
        content = f"{self.shared.__dict__}"
        return content.encode("utf8")  #Default encoding in bytes

    def do_HEAD(self):
        self._set_headers()

def run(sharedData,server_class=HTTPServer, handler_class=Server, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    handler_class._set_shared_object(handler_class,shared=sharedData)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()
