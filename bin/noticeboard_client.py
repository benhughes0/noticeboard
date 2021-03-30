#!/usr/bin/env python3
import socket
import argparse

s = socket.socket()

# Parse args
parser = argparse.ArgumentParser(description='Connect to server')
# --host
parser.add_argument('--host', default='127.0.0.1', type=str,
                    help='host to connect to')
# --port
parser.add_argument('--port', default=12345, type=int,
                    help='host port to connect to')
# --echo
parser.add_argument('--echo', default="echo", type=str,
                    help='string to echo back')

args = parser.parse_args()
host = args.host
port = args.port
string_to_echo = args.echo

s.connect((host, port))
print(s.recv(1024).decode('utf-8'))
s.send((string_to_echo).encode('utf-8'))
print(s.recv(1024).decode('utf-8'))
s.close()
