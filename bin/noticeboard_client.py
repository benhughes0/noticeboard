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
# --message
parser.add_argument('--message', default="Hello World!", type=str,
                    help='string to echo back')

# --action
parser.add_argument('--action', default="echo", type=str,
                    help='action to perform')

args = parser.parse_args()
host = args.host
port = args.port
action = args.action
message = args.message

s.connect((host, port))

msg = recv_message(s)
if msg["status"] == "ok":
    print(msg["message"])
else:
    print("ERROR: %s" % msg["error"])

request = {
    "action" : action,
    "message" : message
}
send_message(s, request)

msg = recv_message(s)
if msg["status"] == "ok":
    print(msg["message"])
else:
    print("ERROR: %s" % msg["error"])

s.close()
