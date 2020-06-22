#!/usr/bin/env python
import socket, sys, os

def interpret_smtp_status_code(resp):
    code = int(resp.split(' ')[0])
    messages = {
        250:'Requested mail action okay, completed', 
        251:'User not local; will forward to <forward-path>', 
        252:'Cannot VRFY user, but will accept message and attempt delivery', 
        502:'Command not implemented', 
        530:'Access denied (???a Sendmailism)', 
        550:'Requested action not taken: mailbox unavailable', 
        551:'User not local; please try <forward-path>', 
    }
    
    if code in messages.keys():
        return f'({code} {messages[code]})'
    else:
        return resp

ip = sys.argv[1]
port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    banner = sock.recv(1024).decode('utf-8')
    
    if 'SMTP' in banner:
        for user in open("unix-users.txt", "r"):
            sock.send(str.encode(f'VRFY {user}'))
            resolution = interpret_smtp_status_code(sock.recv(1024).decode('utf-8'))
            print(f'VRFY {user} ==> {resolution}')
    else:
        print('SMTP service not running on this port.')

    sock.close()
except socket.error:
    print('Connection failed with {} / {}'.format(ip, port))