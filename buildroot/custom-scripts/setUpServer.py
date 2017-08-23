#!/usr/bin/python

import time
import BaseHTTPServer
import platform
import sys
import os
import time
import subprocess
import re
from time import sleep

HOST_NAME = '0.0.0.0' 
PORT_NUMBER = 8080 


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

        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                s.wfile.write(re.sub( ".*model name.*:", "", line,1))
            if "cpu MHz" in line:
                s.wfile.write(re.sub( ".*cpu MHz.*:", "", line,1))

        s.wfile.write("<h4>Capacidade ocupada do processador</h4>")
        last_idle = last_total = 0
        for x in range(3):
            with open('/proc/stat') as f:
                fields = [float(column) for column in f.readline().strip().split()[1:]]
                idle, total = fields[3], sum(fields)
                idle_delta, total_delta = idle - last_idle, total - last_total
                last_idle, last_total = idle, total
                utilisation = 100.0 * (1.0 - idle_delta / total_delta)
                if x==2: s.wfile.write('%5.1f%%' % utilisation)
                sleep(3)


        s.wfile.write("<h4>Quantidade de memoria RAM total</h4>")
        meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
        mem_kb = meminfo['MemTotal']
        s.wfile.write(mem_kb*0.001)

        s.wfile.write("<h4>Quantidade de memoria RAM usada</h4>")
        memFree_kb = meminfo['MemAvailable'] #MemFree
        s.wfile.write((mem_kb-memFree_kb)*0.001)

        s.wfile.write("<h4>Versao do sistema</h4>")
        s.wfile.write(platform.platform())

        s.wfile.write("<h4>Lista dos processos em execucao</h4>")
        processoutput = os.popen("ps -Af").read()
        s.wfile.write(processoutput)
        # TO DO

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

