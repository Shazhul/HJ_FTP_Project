# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import sys
import socket
from os import listdir
from os.path import isfile
from cmds import FTP_COMMANDS

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <SERVER_PORT>" 
	exit(0)


def recvEphyConn(startSock):
	ephyPort = unpad(recvAll(startSock, 5))
	startSock.sendall('1')
	ephySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ephySock.connect(('localhost', int(ephyPort)))
	return ephySock

def pad(s, length):
    padding = '&'
    s = str(s)
    if len(s) < length:
        s = s+ (length - len(s))*padding
    return s

def unpad(s):
	padding = '&'
	return s.strip(padding)

def GetListInDirectory():
	p = listdir('.')
	s = ''
	for f in p:
		s = s + f + '\n'
	return s

def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""
	# The temporary buffer
	tmpBuff = ""
	# Keep receiving till all is received
	while len(recvBuff) < int(numBytes):
		# Attempt to receive bytes
		tmpBuff =  sock.recv(int(numBytes))
		# The other side has closed the socket
		if not tmpBuff:
			break
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	return recvBuff

def ls(ephyconn):
	fileList = GetListInDirectory()
	fileListSize = len(fileList)
	ephyconn.sendall(pad(fileListSize, 1024))
	recvAll(ephyconn, 1)
	ephyconn.sendall(fileList, fileListSize)
	recvAll(ephyconn, 1)

def main():
	welcomePort = int(sys.argv[1])
	# Create a welcome socket. 
	welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	welcomeSock.bind(('', welcomePort))
	# Start listening on the socket
	welcomeSock.listen(10)
	# Accept connections forever
	while True:
		
		print "Waiting for connections..."
		# Accept connections
		clientSock, addr = welcomeSock.accept()
		print "Accepted connection from client: ", addr, "\n"
		
		while 1:
			# The size of the incoming command
			cmd = unpad(recvAll(clientSock, 1024))
			clientSock.sendall('1')
			if(cmd[0:2] == 'ls'):
				# Get the ephy port
				ephyconn = recvEphyConn(clientSock)
				ls(ephyconn)
				ephyconn.close()

			if(cmd[0:3] == 'get'):
				ephyconn = recvEphyConn(clientSock)
				cmdList = cmd.split()
				fileName = cmdList[1]
				s = open(fileName, 'r').read()
				ephyconn.sendall(pad(len(s), 1024))
				recvAll(ephyconn, 1)
				ephyconn.sendall(s)
				recvAll(ephyconn, 1)
				ephyconn.close()

			if(cmd[0:3] == 'put'):
				ephyconn = recvEphyConn(clientSock)
				cmdList = cmd.split()
				fileName = cmdList[1]
				f = open(fileName, 'w')
				slen = unpad(recvAll(ephyconn, 1024))
				ephyconn.sendall('1')
				s = recvAll(ephyconn, slen)
				ephyconn.sendall('1')
				ephyconn.close()
				f.write(s)
				f.close()

		# Close our side
		clientSock.close()

if __name__ == "__main__":
	main()

