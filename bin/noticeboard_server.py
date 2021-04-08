#!/usr/bin/env python3
import socket
import argparse
import time
import threading
import queue
import logging
from nblib import send_message, recv_message

DEFAULT_PORT = 12345
DEFAULT_WORKER_COUNT = 3
DEFAULT_HOST = "127.0.0.1"
DEFAULT_TIMEOUT = 13        # use prime as timeout
LISTEN_QUEUE_SIZE = 5       # how many connection requests to queue for listen()

s = socket.socket()         # Create a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# host_name = socket.gethostname()
# avoid error
#   socket.gaierror: [Errno 8] nodename nor servname provided, or not known
host_name = DEFAULT_HOST
host_ip = socket.gethostbyname(host_name)

# Parse args
parser = argparse.ArgumentParser(description='Run noticeboard server')
# --host
parser.add_argument('--host', default=host_ip, type=str,
                    help='host to connect to')
# --port n
parser.add_argument('--port', default=DEFAULT_PORT, type=int,
                    help='host port to connect to')
# --workers n
parser.add_argument('--workers', default=DEFAULT_WORKER_COUNT, type=int,
                    help='number of worker threads')

# Set up logging
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

args = parser.parse_args()

host = args.host
port = args.port
num_workers = args.workers

# generic worker
def worker(q, handler):
    while True:
        try:
            job = q.get(timeout=DEFAULT_TIMEOUT)
        except queue.Empty:
            continue
        handler(job)
        q.task_done()

def output_handler(request):
    logging.info(request)

output_q = queue.Queue()
def output(text):
    output_q.put_nowait(text)

output_thread = threading.Thread(target=worker, args=[output_q, output_handler], daemon=True)
output_thread.start()

output("host_name: %s" % host_name)
output("host_ip: %s" % host_ip)
output("host: %s" % host)
output("port: %s" % port)

# Global store for messages
MESSAGES = {}
REPLIES = {}

def new_message(text):
    return [text, []]

def handle_request(request):
    action = request["action"]
    request_id = request["request_id"]

    if action == "echo":
        output("They said '%s'" % request["message"])
        text = 'You said %s' % request["message"]
        response = {
            "status" : "ok",
            "message" : text
        }
    elif action == "post":
        MESSAGES[request_id] = new_message(request["message"])
        response = {
            "status" : "ok",
            "id" : request_id
        }
    elif action == "readall":
        response = {
            "status" : "ok",
            "messages" : MESSAGES
        }
    elif action == "read":
        msg_id = request["id"]
        response = {
            "status" : "ok",
            "message" : MESSAGES[msg_id]
        }
    elif action == "reply":
        msg_id = request["id"]
        msg = MESSAGES[msg_id]

        REPLIES[request_id] = request["message"]
        msg[-1].append(REPLIES[request_id])

        response = {
            "status" : "ok",
            "id" : request_id
        }
    elif action == "remove":
        msg_id = request["id"]
        if msg_id in MESSAGES:
            del MESSAGES[msg_id]
        if msg_id in REPLIES:
            del REPLIES[msg_id]
        response = {
            "status" : "ok",
            "message" : "Message %s removed" % msg_id
        }
    else:
        text = "Unknown action: '%s'" % action
        output(text)
        response = {
            "status" : "error",
            "reason" : text
        }

    return response

def request_handler(job):
    request_id, conn = job

    request = recv_message(conn)
    request["request_id"] = request_id

    msg = handle_request(request)
    send_message(conn, msg)
    conn.close()                # Close the connection

jobq = queue.Queue()
for i in range(num_workers):
    t = threading.Thread(target=worker, args=[jobq, request_handler], daemon=True)
    t.start()

s.bind((host, port))        # Bind to the port

s.listen(LISTEN_QUEUE_SIZE) # Now wait for client connection.
request_id = 0
while True:
    try:
        conn, addr = s.accept()     # Establish connection with client.
        request_id += 1
        output('%04d: Got connection from %s' % (request_id, addr))
        jobq.put_nowait((request_id, conn))
    except:
        break
print("Server ending")
