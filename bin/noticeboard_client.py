#!/usr/bin/env python3
import socket
import argparse
from nblib import send_message, recv_message

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

request = {
    "action" : action,
    "message" : message
}
send_message(s, request)

response = recv_message(s)
if response["status"] == "ok":
    if action == "echo":
        print(response["message"])
    elif action == "post":
        print(response["id"])
    elif action == "readall":
        print(response["messages"])
    else:
        print(response)
else:
    print("ERROR: %s" % response["reason"])

s.close()
