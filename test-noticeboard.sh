#!/bin/sh
bin/noticeboard_server.py > /dev/null 2>&1 &
SERVER_PID=$!
sleep 0.5
./test-create-messages.sh > output.txt
kill $SERVER_PID > /dev/null 2>&1

diff output.txt expected-output.txt
