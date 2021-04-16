#!/usr/bin/env python3
import socket
import argparse
from nblib import send_message, recv_message

# Parse args
parser = argparse.ArgumentParser(description='command line client for noticeboard')
subparsers = parser.add_subparsers(dest='action',help='sub-command help')

parser_post = subparsers.add_parser('post', help='post a message')
parser_post.add_argument('message', type=str, help='string of text to post')

parser_read = subparsers.add_parser('read', help='read a specific message')
parser_read.add_argument('id', type=int, help='id of the message to read')

parser_readall = subparsers.add_parser('readall', help='read all messages on the board')

parser_reply = subparsers.add_parser('reply', help='reply to a message')
parser_reply.add_argument('id', type=int, help='id of message to reply to')
parser_reply.add_argument('message', type=str, help='string of text to reply with')

parser_remove = subparsers.add_parser('remove', help='remove a message from the board')
parser_remove.add_argument('id', type=int, help='id of the message to remove')

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

s = socket.socket()
s.connect((host, port))

request = {
    "action" : action,
    "message" : message,
    "id" : args.id
}
send_message(s, request)

response = recv_message(s)
# print(str(response))
if response["status"] == "ok":
    if action == "echo":
        print(response["message"])
    elif action == "post":
        print("Posted message %s" % (response["id"]))
    elif action == "readall":
        for msg_id, msg in response["messages"].items():
           print("%s: %s" % (msg_id, msg["message"]))
           for reply_id, reply in msg["replies"].items():
               print("\t%s: %s" % (reply_id, reply))
    elif action == "read":
        print("%s: %s" % (args.id,response["message"]["message"]))
        for reply_id, reply in response["message"]["replies"].items():
            print("\t%s: %s" % (reply_id, reply))
    elif action == "reply":
        print("Posted message %s" % (response["id"]))
    elif action == "remove":
        print(response["message"])
    else:
        print(response)
else:
    print("ERROR: %s" % response["reason"])

s.close()
