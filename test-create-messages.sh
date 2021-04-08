#!/bin/sh
echo ADD messages
for i in {1..3}; do
  bin/noticeboard_client.py --action post --message "Message $i"
done
echo READALL
bin/noticeboard_client.py --action readall
echo REPLY to message 1
bin/noticeboard_client.py --action reply --id 1 --message "Hello"
bin/noticeboard_client.py --action reply --id 1 --message "World"
echo READ message 1
bin/noticeboard_client.py --action read --id 1
echo REMOVE reply 5
bin/noticeboard_client.py --action remove --id 5
echo READ message 1
bin/noticeboard_client.py --action read --id 1
echo REMOVE message 1
bin/noticeboard_client.py --action remove --id 1
echo READALL
bin/noticeboard_client.py --action readall
echo REPLY to removed message 1
bin/noticeboard_client.py --action reply --id 1 --message "Hello"
