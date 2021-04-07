#!/usr/bin/env python3
import socket
import argparse
import time
import threading
import queue
import logging
import json

DEFAULT_PORT = 12345
DEFAULT_WORKER_COUNT = 3
DEFAULT_HOST = "127.0.0.1"
DEFAULT_TIMEOUT = 13        # use prime as timeout
LISTEN_QUEUE_SIZE = 5       # how many connection requests to queue for listen()
MAX_SIZE = 65535

# Helper functions for sending and receiving JSON messages
def send_message(conn, msg):
    return conn.send(json.dumps(msg).encode('utf-8'))

def recv_message(conn):
    json_str = conn.recv(MAX_SIZE).decode('utf-8')
    return json.loads(json_str)

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

def handle_output(request):
    logging.info(request)

def worker_output(output_q):
    worker(output_q, handle_output)

output_q = queue.Queue()
def output(text):
    output_q.put_nowait(text)

output_thread = threading.Thread(target=worker_output, args=[output_q], daemon=True)
output_thread.start()

output("host_name: %s" % host_name)
output("host_ip: %s" % host_ip)
output("host: %s" % host)
output("port: %s" % port)

def handle_request(job):
    request_id, conn = job

    msg = {
        "status" : "ok",
        "message" : "Thank you for connecting to " + host
    }
    send_message(conn, msg)

    request = recv_message(conn)
    output("They said '%s'" % request["message"])
    text = '%04d: You said %s' % (request_id, request["message"])
    msg = {
        "status" : "ok",
        "message" : text
    }
    send_message(conn, msg)
    conn.close()                # Close the connection

def worker_job(q):
    worker(q, handle_request)

jobq = queue.Queue()
for i in range(num_workers):
    t = threading.Thread(target=worker_job, args=[jobq], daemon=True)
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
