#!/usr/bin/env python
import socket, subprocess, sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

remoteServer = sys.argv[1]
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
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            try:
                sockBanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sockBanner.settimeout(1)
                sockBanner.connect((remoteServerIP, port))
                banner = sockBanner.recv(1024)
                sockBanner.close()
                print(f"Porta {port} | {banner}")
            except socket.timeout:
                print(f"Porta {port} | Serviço não retornou banner.")

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