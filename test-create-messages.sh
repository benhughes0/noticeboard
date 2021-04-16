#!/usr/bin/env bash
# Simple script to test each available action
NB_CLIENT="bin/nb.py --debug"
echo POST messages
for i in {1..3}; do
  $NB_CLIENT --action post --message "Message $i"
done
echo READALL
$NB_CLIENT --action readall
echo REPLY to message 1
$NB_CLIENT --action reply --id 1 --message "Hello"
$NB_CLIENT --action reply --id 1 --message "World"
echo READ message 1
$NB_CLIENT --action read --id 1
echo REMOVE reply 5
$NB_CLIENT --action remove --id 5
echo READ message 1
$NB_CLIENT --action read --id 1
echo REMOVE message 1
$NB_CLIENT --action remove --id 1
echo READALL
$NB_CLIENT --action readall
echo REPLY to removed message 1
$NB_CLIENT --action reply --id 1 --message "Hello"
echo UNKNOWN action
$NB_CLIENT --action foo --id 1 --message "Foo"
