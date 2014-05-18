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


print 'sending marco'
#Send command
commandSock.send('Marco')
print 'marco sent'
#Accept data
print 'Waiting for response'
resp = commandSock.recv(1024)
print resp

#Close main socket
mainSock.close()
#Close command socket
commandSock.close()
print 'Exiting'
