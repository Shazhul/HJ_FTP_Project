# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import os
import sys
import socket
from netfunc import *

# Command line checks 
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER_MACHINE> <SERVER_PORT>"
	exit(0)

def ls(ephyconn):
	fileListSize = unpad(recvAll(ephyconn, DEFAULT_SEND_SIZE))
	ephyconn.sendall('1')
	fileList = recvAll(ephyconn, (int(fileListSize)-1))
	ephyconn.sendall('1')
	print(fileList)

def main():
	#Server address
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

	# Keep sending until all is sent
	while True:
		cmd  = raw_input("ftp> ")
		
		if(cmd == 'exit'):
			commandSock.sendall(pad(cmd, DEFAULT_SEND_SIZE))
			success = recvAll(commandSock, ACK_SIZE)
			break
		
		if(verifyCommand(cmd)):
		#Send the command
			try:
				commandSock.sendall(pad(cmd, DEFAULT_SEND_SIZE))
				success = recvAll(commandSock, ACK_SIZE)
			except:
				print('Error sending command')

			if(cmd[0:2] == 'ls'):
				ephyconn = setupEphyConn(commandSock)
				try:
					ls(ephyconn)
				except:
					print('Error calling ls')
				ephyconn.close()

			elif(cmd[0:3] == 'get'):
				ephyconn = setupEphyConn(commandSock)
				try:
					recvFile(ephyconn, cmd.split()[1])
				except:
					print('Error calling get')
				ephyconn.close()

			elif(cmd[0:3] == 'put'):
				ephyconn = setupEphyConn(commandSock)
				try:
					sendFile(ephyconn, cmd.split()[1])
				except:
					print('Error calling put')
				ephyconn.close()
			else:
				break
		else:
			print('Invalid command')

	commandSock.close()

if __name__ == "__main__":
	main()

