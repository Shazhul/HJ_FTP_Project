# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import sys
import socket
from cmds import FTP_COMMANDS

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <SERVER_PORT>" 
	exit(0)

welcomePort = int(sys.argv[1])

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', welcomePort))

# Start listening on the socket
welcomeSock.listen(10)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < int(numBytes):
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff
		
# Accept connections forever
while True:
	
	print "Waiting for connections..."
	# Accept connections
	clientSock, addr = welcomeSock.accept()
	print "Accepted connection from client: ", addr, "\n"
	
	# The size of the incoming command
	cmdSize = recvAll(clientSock, 4)
	#get the size of the inc command	

	# Receive the first 10 bytes indicating the
	# size of the command
	cmdBuff = recvAll(clientSock, cmdSize)
	serverCmd = FTP_COMMANDS(cmdBuff)
	
	if serverCmd.isCommand:
		serverCmd.RunCommand(ftpconnection)
		
# Close our side
clientSock.close()
	
