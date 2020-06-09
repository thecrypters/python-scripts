#!/usr/bin/env python
import socket
import subprocess
import sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

remoteServer    = input("Informe um nome de HOST remoto para o Scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)  # traduz o nome do host para IPv4

print("-" * 60)
print("Escaneando o IP: ", remoteServerIP)
print("-" * 60)

tInicio = datetime.now()

try:
    for port in range(1,1000):
        '''
            AF_INET => Socket Family
            SOCK_STREAM => Socket type for TCP connections
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((remoteServerIP, port))
        status = "Open" if result == 0 else "Close"
        print(f"Port {port} | Status {status}")
        sock.close()

except KeyboardInterrupt:
    print("You pressed Ctrl+C")
    sys.exit()

except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

except socket.error:
    print("Couldn't connect to server")
    sys.exit()

tFim = datetime.now()
tempoTotal =  tFim - tInicio
print('Escaneamento completo em: ', tempoTotal)
