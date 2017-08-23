#!/usr/bin/python

import time
import BaseHTTPServer
import platform
import sys
import os
import time

HOST_NAME = '0.0.0.0' 
PORT_NUMBER = 8080 


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    last_worktime=0
    last_idletime=0

# MARK: get infomration from OS
    def get_cpu():
        global last_worktime, last_idletime
        f=open("/proc/stat","r")
        line=""
        while not "cpu " in line: line=f.readline()
        f.close()
        spl=line.split(" ")
        worktime=int(spl[2])+int(spl[3])+int(spl[4])
        idletime=int(spl[5])
        dworktime=(worktime-last_worktime)
        didletime=(idletime-last_idletime)
        rate=float(dworktime)/(didletime+dworktime)
        last_worktime=worktime
        last_idletime=idletime
        if(last_worktime==0): return 0
        return rate

    def memory_usage_ps():
        import subprocess
        out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
        stdout=subprocess.PIPE).communicate()[0].split(b'\n')
        vsz_index = out[0].split().index(b'RSS')
        mem = float(out[1].split()[vsz_index]) / 1024
        return mem


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
        # command = "cat /proc/cpuinfo"
        #         all_info = subprocess.check_output(command, shell=True).strip()
        #         for line in all_info.split("\n"):
        #             if "model name" in line:
        #                 s.wfile.write(re.sub( ".*model name.*:", "", line,1))
        # return subprocess.check_output(command, shell=True).strip()
        s.wfile.write(subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip())

        s.wfile.write("<h4>Capacidade pocupada do processador</h4>")
        # s.wfile.write(get_cpu())
        
        # def read_cpu_usage(stat_path='/proc/stat'):
        #     with open(stat_path) as stat_file:
        #         return sum(float(time) for time in next(stat_file).split()[1:])
        # s.wfile.write(read_cpu_usage())


        s.wfile.write("<h4>Quantidade de memoria RAM total</h4>")
        # meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
        # mem_kib = meminfo['MemTotal']
        # s.wfile.write(mem_kib)

        s.wfile.write("<h4>Quantidade de memoria RAM usada</h4>")
        # s.wfile.write(memory_usage_ps())

        s.wfile.write("<h4>Versao do sistema</h4>")
        s.wfile.write(platform.platform())

        s.wfile.write("<h4>Lista dos processos em execucao</h4>")
        # pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        # for pid in pids:
        #     try:
        #         s.wfile.write(open(os.path.join('/proc', pid, 'cmdline'), 'rb').read())
        #     except IOError: # proc has already terminated
        #         continue
        
        # processoutput = os.popen("ps -Af").read()
        # s.wfile.write(processoutput)
        
        # s.wfile.write(os.system("ps"))
        
        # def get_pname(id):
        #     p = subprocess.Popen(["ps -o cmd= {}".format(id)], stdout=subprocess.PIPE, shell=True)
        #     return str(p.communicate()[0])
        # name = get_pname(1)
        # s.wfile.write(name)

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

