#!/bin/sh
# Compare actual and expected output of test-create-messages.sh
#
# Launch noticeboard_server.py
bin/noticeboard_server.py > /dev/null 2>&1 &
SERVER_PID=$!
trap "kill $SERVER_PID > /dev/null 2>&1" EXIT
sleep 0.5
# Run test script
./test-create-messages.sh > output.txt
# Diff output
diff output.txt expected-output.txt
