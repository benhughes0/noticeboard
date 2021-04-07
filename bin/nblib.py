# nblib - lib of shared functions for noticeboard
import json

MAX_MSG_SIZE = 65535

def send_message(conn, msg):
    return conn.send(json.dumps(msg).encode('utf-8'))

def recv_message(conn):
    json_str = conn.recv(MAX_MSG_SIZE).decode('utf-8')
    return json.loads(json_str)
