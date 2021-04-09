#!/bin/sh
# Compare actual and expected output of test-create-messages.sh
#
# Launch noticeboard_server.py
bin/noticeboard_server.py > /dev/null 2>&1 &
SERVER_PID=$!
sleep 0.5
# Run test script
./test-create-messages.sh > output.txt
# Kill server
kill $SERVER_PID > /dev/null 2>&1
# Diff output
diff output.txt expected-output.txt
