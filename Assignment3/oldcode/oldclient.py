# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import os
import sys
import socket
from cmds import FTP_COMMANDS

# Command line checks 
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER_MACHINE> <SERVER_PORT>"
	exit(0)

# Server address
serverAddr = socket.gethostbyname(sys.argv[1])

# Server port
serverPort = int(sys.argv[2])

# Create a command TCP socket
commandSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect both sockets to the server
try:
	commandSock.connect((serverAddr, serverPort))
except:
	print("Could not connect")
	exit(0)

# The number of bytes sent
numSent = 0

# Keep sending until all is sent
while True:
	cmd  = raw_input("ftp> ")
	
	if(cmd == 'exit'):
		print('Exiting')
		break

	newCmd = FTP_COMMANDS(cmd)

	if newCmd.isCommand:
		newCmd.RunCommand(commandSock)
	
commandSock.close()
