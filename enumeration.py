#!/usr/bin/python

import socket
import sys

filename = sys.argv[2]
with open(filename) as f:
    users = [line.strip() for line in f.readlines() if line]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((sys.argv[1], 25))
fn = s.makefile('rwb')

fn.readline()                
fn.write('HELO testing.com \r\n')
fn.flush()
fn.readline()

for user in users:
    fn.write('VRFY %s\r\n' % user)
    fn.flush()
    print('%s: %s' % (user, fn.readline().strip()))

fn.write('QUIT\r\n')
fn.flush()