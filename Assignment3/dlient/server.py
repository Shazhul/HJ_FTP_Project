# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import sys
import socket
from os import listdir
from os.path import isfile
from netfunc import *
from multiprocessing import Process

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <SERVER_PORT>" 
	exit(0)

def GetListInDirectory():
	p = listdir('.')
	s = ''
	for f in p:
		s = s + f + '\n'
	return s

def ls(ephyconn):
	fileList = GetListInDirectory()
	fileListSize = len(fileList)
	ephyconn.sendall(pad(fileListSize, DEFAULT_SEND_SIZE))
	recvAll(ephyconn, ACK_SIZE)
	ephyconn.sendall(fileList, fileListSize)
	recvAll(ephyconn, ACK_SIZE)
	ephyconn.close()

def serverproc(port, addr):
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSock.connect((addr[0], int(port)))
	while True:
		# The size of the incoming command
		try:
			cmd = unpad(recvAll(clientSock, DEFAULT_SEND_SIZE))
			clientSock.sendall('1')
		except:
			print('Error receiving command')
			break
		
		if(cmd == 'exit'):
			break

		if(verifyCommand(cmd)):
			if(cmd[0:2] == 'ls'):
				# Get the ephy port
				ephyconn = recvEphyConn(clientSock, addr)
				try:
					ls(ephyconn)
				except:
					print('Error calling ls')

			elif(cmd[0:3] == 'get'):
				ephyconn = recvEphyConn(clientSock, addr)
				try:
					sendFile(ephyconn, cmd.split()[1])
				except:
					print('Error calling get')

			elif(cmd[0:3] == 'put'):
				ephyconn = recvEphyConn(clientSock, addr)
				try: 
					recvFile(ephyconn, cmd.split()[1])
				except: 
					print('Error calling put')
	clientSock.close()

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
		port = unpad(recvAll(clientSock, SOCKET_SEND_SIZE))
		clientSock.sendall('1')
		p = Process(target=serverproc, args=(port, addr,))
		p.start()

if __name__ == "__main__":
	main()

