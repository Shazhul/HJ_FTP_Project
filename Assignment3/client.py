# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import os
import sys
import socket

# Command line checks 
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER_MACHINE> <SERVER_PORT>"
	exit(0)

def ls(ephyconn):
	fileListSize = unpad(recvAll(ephyconn, 1024))
	ephyconn.sendall('1')
	fileList = recvAll(ephyconn, (int(fileListSize)-1))
	ephyconn.sendall('1')
	print(fileList)

def pad(s, length):		
	padding = '&'
	s = str(s)
	if len(s) < length:
		s = s+ (length - len(s))*padding
	return s

def unpad(s):
    padding = '&'
    return s.strip(padding)

	#Get the list of files
def setupEphyConn(startSock):
	ephySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ephySock.bind(('localhost',0))
	ephySock.listen(1)
	ephyPort = ephySock.getsockname()[1]
	#Sending 5 bytes
	startSock.sendall(pad(ephyPort, 5))
	success = recvAll(startSock, 1)
	ephyconn, ephyaddress = ephySock.accept()
	return ephyconn

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
			print('Exiting')
			break

		if(cmd == 'ls'):
			#Send the command size - 1 byte
			commandSock.sendall('2')
			success = recvAll(commandSock, 1)
			#Send the command - cmdsize bytes
			commandSock.sendall(cmd)
			success = recvAll(commandSock, 1)
			ephyconn = setupEphyConn(commandSock)
			ls(ephyconn)
			ephyconn.close()

		if(cmd == 'get'):
			pass#getfile()

		if(cmd == 'put'):
			pass#putfile()

	commandSock.close()

if __name__ == "__main__":
	main()

