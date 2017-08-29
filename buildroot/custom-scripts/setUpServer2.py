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

        # Data e Hora
        s.wfile.write("<h4>Data e hora do sistema</h4>")

        def getDataTime():
            d = time.strftime("%d/%m/%Y")
            t = time.strftime("%H:%M:%S")
            return "Date:" + d + " Time:" + t
        s.wfile.write(getDataTime())

        # Uptime
        s.wfile.write("<h4>Uptime em segundos</h4>")

        def getUptime():
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return uptime_seconds

        s.wfile.write(getUptime())

        # Modelo Processador
        s.wfile.write("<h4>Modelo do processador e velocidade</h4>")

        def getCPUModel():
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).strip()
            n = ""
            v = ""
            for line in all_info.split("\n"):
                if "model name" in line:
                    n = re.sub( ".*model name.*:", "", line,1)
                if "cpu MHz" in line:
                    v = re.sub( ".*cpu MHz.*:", "", line,1)
            return n + " " + v
        s.wfile.write(getCPUModel())

        # Capacidade Ocupada Processador
        s.wfile.write("<h4>Capacidade ocupada do processador</h4>")
        def getCPUUsage():
            last_idle = last_total = 0
            for x in range(3):
                with open('/proc/stat') as f:
                    fields = [float(column) for column in f.readline().strip().split()[1:]]
                    idle, total = fields[3], sum(fields)
                    idle_delta, total_delta = idle - last_idle, total - last_total
                    last_idle, last_total = idle, total
                    utilisation = 100.0 * (1.0 - idle_delta / total_delta)
                    if x==2: return ('%5.1f%%' % utilisation)
                    sleep(3)

        s.wfile.write(getCPUUsage())

        # Memoria RAM Total
        s.wfile.write("<h4>Quantidade de memoria RAM total</h4>")

        def getRAMSize():
            meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
            mem_kb = meminfo['MemTotal']
            return (mem_kb*0.001)
        s.wfile.write(getRAMSize)

        # Memoria RAM Usada
        s.wfile.write("<h4>Quantidade de memoria RAM usada</h4>")
        def getRAMFree():
            meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
            mem_kb = meminfo['MemTotal']
            memFree_kb = meminfo['MemAvailable'] #MemFree
            return ((mem_kb-memFree_kb)*0.001)

        s.wfile.write(getRAMFree())

        # Versao do Sistema
        s.wfile.write("<h4>Versao do sistema</h4>")

        def getOSVersion():
            return platform.platform()

        s.wfile.write(getOSVersion())

        # Processos em Execucao
        s.wfile.write("<h4>Lista dos processos em execucao</h4>")
        def getProcesses():
            processoutput = os.popen("ps -Af").read()
            # TO DO - parse data
            return processoutput
        
        s.wfile.write(getProcesses())

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

