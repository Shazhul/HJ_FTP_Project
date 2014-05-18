import socket
import time

#Initiate connection
mainSock = socket.socket()
host = socket.gethostname()
port = 2000
mainSock.connect((host, port))

print 'Connected'

#Receive port number
portNum = int(mainSock.recv(1024))
print portNum

time.sleep(1)

commandSock = socket.socket()
#Connect to port number
commandSock.connect((host, portNum))

#Close main socket
mainSock.close()
print 'sending marco'
#Send command
commandSock.send('Marco')
print 'marco sent'
#Accept data
print commandSock.recv(1024)

#Close connection
commandSock.close()
print 'Exiting'
