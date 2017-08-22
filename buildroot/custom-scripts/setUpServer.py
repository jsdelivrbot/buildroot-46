#!/usr/bin/python

import time
import BaseHTTPServer
import platform
import sys
import os
import time

HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>LabSisp - T1 - BK</title></head>")
        s.wfile.write("<body><h1>Laboratorio de Sistemas Operacionais TP1</h1>")
        s.wfile.write("<p>Barbara Kudiess</p>")

        s.wfile.write("<h4>Data e hora do sistema</h4>")
        s.wfile.write(time.strftime("%d/%m/%Y"))
        s.wfile.write(time.strftime("%H:%M:%S"))

        s.wfile.write("<h4>Uptime em segundos</h4>")
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        s.wfile.write(uptime_seconds)

        s.wfile.write("<h4>Modelo do processador e velocidade</h4>")

        s.wfile.write("<h4>Capacidade pocupada do processador</h4>")

        s.wfile.write("<h4>Quantidade de memoria RAM total</h4>")

        s.wfile.write("<h4>Quantidade de memoria RAM usada</h4>")

        s.wfile.write("<h4>Versao do sistema</h4>")
        s.wfile.write(platform.platform())

        s.wfile.write("<h4>Lista dos processos em execucao</h4>")

        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

