#!/usr/bin/env python3
import socket
import argparse
from nblib import send_message, recv_message

s = socket.socket()

# Parse args
parser = argparse.ArgumentParser(description='Connect to server')
subparsers = parser.add_subparsers(dest='action',help='sub-command help')

parser_post = subparsers.add_parser('post', help='print help')
parser_post.add_argument('message', type=str, help='message help')

parser_read = subparsers.add_parser('read', help='read help')
parser_read.add_argument('id', type=int, help='id help')

parser_readall = subparsers.add_parser('readall', help='readall help')

parser_reply = subparsers.add_parser('reply', help='reply help')
parser_reply.add_argument('id', type=int, help='id help')
parser_reply.add_argument('message', type=str, help='message help')

parser_remove = subparsers.add_parser('remove', help='remove help')
parser_remove.add_argument('id', type=int, help='id help')

# --host
parser.add_argument('--host', default='127.0.0.1', type=str,
                    help='host to connect to')
# --port
parser.add_argument('--port', default=12345, type=int,
                    help='host port to connect to')
# --message
parser.add_argument('--message', default="Hello World!", type=str,
                    help='string to echo back')

# --id
parser.add_argument('--id', default=0, type=int,
                    help='id of message to act on')

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
    "message" : message,
    "id" : args.id
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
        # for k, v in response["messages"]:
        #    print("%4s : %s" % (k, v))
    elif action == "read":
        print(response["message"])
    else:
        print(response)
else:
    print("ERROR: %s" % response["reason"])

s.close()
