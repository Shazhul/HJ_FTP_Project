import socket
#The size of ephyports's size
SOCKET_SEND_SIZE = 5
#The size of our acks
ACK_SIZE = 1
#The size of the message sent to tell the size of the next object
DEFAULT_SEND_SIZE = 1024

def pad(s, length):
    padding = '\0'
    s = str(s)
    if len(s) < length:
        s = s+ (length - len(s))*padding
    return s

def unpad(s):
    padding = '\0'
    return s.strip(padding)

    #Get the list of files
def setupEphyConn(startSock):
    ephySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ephySock.bind(('localhost',0))
    ephySock.listen(1)
    ephyPort = ephySock.getsockname()[1]
    startSock.sendall(pad(ephyPort, SOCKET_SEND_SIZE))
    success = recvAll(startSock, ACK_SIZE)
    ephyconn, ephyaddress = ephySock.accept()
    return ephyconn

def recvEphyConn(startSock, addr):
    ephyPort = unpad(recvAll(startSock, SOCKET_SEND_SIZE))
    startSock.sendall('1')
    ephySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ephySock.connect((addr[0], int(ephyPort)))
    return ephySock

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

def verifyCommand(cmd):
    if len(cmd) < 2:
        return False
    if cmd[0:2] == 'ls':
        return True
    if len(cmd) < 3:
        return False
    if cmd[0:3] == 'get':
        if len(cmd.split()) < 2:
            print 'USAGE: get <filename>'
            return False
        else:
            return True
    if cmd[0:3] == 'put':
        if len(cmd.split()) < 2:
            print 'USAGE: put <filename>'
            return False
        else:
            return True
	if cmd == 'exit':
		return True
    return False

def sendFile(ephyconn, fileName):
	print'sending file'
	try:
		data = open(fileName, 'r').read()
	except:
		print('Error opening file for reading')
		ephyconn.sendall(pad('0', DEFAULT_SEND_SIZE)) 
		recvAll(ephyconn, ACK_SIZE)
		return 
	ephyconn.sendall(pad(len(data), DEFAULT_SEND_SIZE))
	recvAll(ephyconn, ACK_SIZE)
	ephyconn.sendall(data)
	recvAll(ephyconn, ACK_SIZE)
	ephyconn.close()
	print 'file sent'

def recvFile(ephyconn, fileName):
	print'getting file'
	datafile = open(fileName, 'w')
	datalen = unpad(recvAll(ephyconn, DEFAULT_SEND_SIZE))
	if(datalen == '0'):
		ephyconn.sendall('1')
		print('File transfer error')
		return
	ephyconn.sendall('1')
	data = recvAll(ephyconn, datalen)
	ephyconn.sendall('1')
	ephyconn.close()
	datafile.write(data)
	datafile.close()
	print 'file got'
