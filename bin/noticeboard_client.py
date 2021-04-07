#!/usr/bin/env python3
import socket
import argparse
import json

MAX_SIZE = 65535

def send_message(conn, msg):
    return conn.send(json.dumps(msg).encode('utf-8'))

def recv_message(conn):
    json_str = conn.recv(MAX_SIZE).decode('utf-8')
    return json.loads(json_str)

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

msg = recv_message(s)
print(msg["message"])

request = {
    "action" : "echo",
    "message" : string_to_echo
}
send_message(s, request)
response = recv_message(s)
print(response["message"])

s.close()
