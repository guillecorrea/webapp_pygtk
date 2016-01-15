#!/usr/bin/python
import BaseHTTPServer, SimpleHTTPServer 
# TODO : agregar comprobacion de user agent y de clave para que solo el visor pueda acceder al servidor . 
s = BaseHTTPServer.HTTPServer(('', 6566), SimpleHTTPServer.SimpleHTTPRequestHandler)
s.serve_forever()
