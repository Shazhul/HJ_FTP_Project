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
import threading

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

tpool = []

def main():
	welcomePort = int(sys.argv[1])
	welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	welcomeSock.bind(('', welcomePort))
	welcomeSock.listen(10)
	while True:
		print "Waiting for connections..."
		# Accept connections
		clientSock, addr = welcomeSock.accept()
		print "Accepted connection from client: ", addr, "\n"
		port = unpad(recvAll(clientSock, SOCKET_SEND_SIZE))
		clientSock.sendall('1')
		t = threading.Thread(target=serverproc, args=(port, addr,))
		t.start()
		for thr in tpool:
			t.join(0.1)

if __name__ == "__main__":
	main()

