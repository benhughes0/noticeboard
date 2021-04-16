## User Guide for the shared command line noticeboard client

The program allows you to post, read and remove anoymous messages on a shared noticeboard. You can also reply to messages in a thread. This user guide will explain how to use the noticeboard python client nb.py to interact with the noticeboard.

To use the client, you should have python installed. While in the root directory of the this repo, all commands will take the form of `python bin/nb.py {action} {arguments}`.

### Reading messages

To see all the messages currently on the noticeboard, use the action 'readall'

`python bin/nb.py readall`

To focus on a single message, use the action 'read' and specify the ID of the message.

`python bin/nb.py read 2`

### Posting and replying

To post a message to the board, use the action 'post', followed by your message, in quotes

`python bin/nb.py post "what time does the shop close?"`

After posting a message, you will be given its unique ID. This can be used to reply to the message or remove it from the board. Messages and users are not tracked, so this ID is the only way to identify your message.

To reply to a message, use the action 'reply' followed by the ID of the message you want to reply to, then your reply in quotes. These arguments should all be seperated by spaces.

`python bin/nb.py reply 5 "I think it shuts at 4pm today"`

*Note: You cannot reply to a reply, only first-level messages.*

### Removing messages

Anyone with access to the shared noticeboard can remove a message or reply. To do this, use the action 'remove', followed by the ID of the message or reply that you want to remove.

`python bin/nb.py remove 5`

*Note: Removing a first-level message will also remove all of the replies have been made in response to it.*

#### Dev: Running the noticeboard server

The noticeboard server is packaged in a docker container, and can be built and run on a machine using these commands:

`docker build -t bh/nb -f ./Dockerfile .`

`docker run -p12345:12345 -it --rm bh/nb`
