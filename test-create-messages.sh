#!/bin/sh
for i in {1..3}; do
  bin/noticeboard_client.py --action post --message "Message $i"
done

bin/noticeboard_client.py --action readall
bin/noticeboard_client.py --action reply --id 1 --message "Hello"
bin/noticeboard_client.py --action reply --id 1 --message "World"
bin/noticeboard_client.py --action read --id 1
