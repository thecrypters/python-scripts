#!/usr/bin/env python
import socket, subprocess, sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

remoteServer = sys.argv[1]
remoteServerIP  = socket.gethostbyname(remoteServer)  # translate hostname to IPv4
portStart = int(sys.argv[2])
portEnd = int(sys.argv[3])


print("-" * 60)
print("Scanning IP: ", remoteServerIP)
print("-" * 60)

labels = []
tStart = datetime.now()

try:
    for port in range(portStart,portEnd+1):
        '''
            AF_INET => Socket Family
            SOCK_STREAM => Socket type for TCP connections
        '''
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            try:
                sockBanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sockBanner.settimeout(1)
                sockBanner.connect((remoteServerIP, port))
                banner = sockBanner.recv(1024)
                sockBanner.close()
                labels.append(f"Port {port} | {banner}")
            except socket.timeout:
                labels.append(f"Port {port} | Service not returned a banner.")

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

tEnd = datetime.now()

for label in labels:
    print(label)

print("-" * 60)
print(f'Scanned {portEnd} ports in {tEnd - tStart}')
print("-" * 60)