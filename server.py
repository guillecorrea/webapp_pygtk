#!/usr/bin/python
import BaseHTTPServer, SimpleHTTPServer 

s = BaseHTTPServer.HTTPServer(('', 6566), SimpleHTTPServer.SimpleHTTPRequestHandler)
s.serve_forever()