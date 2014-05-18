import socket
import multiprocessing
import threading
import time
from multiprocessing import Queue

def CommandConnection(dataConnection, command):
    print 'Thread started'
    print command
    #Thread handles command
    if command == 'Marco':
        connection.send('Polo')
        print 'Sent Polo'
    else:
        connection.send('Invalid command')
        print 'Sent Invalid command'
    
def ClientConnection(dataConnection,address):
    print 'Child started'
        
    print 'Waiting for command'
    #Child listens for data
    command = dataConnection.recv(1024)
    print command

    print 'Starting thread'
    #Child creates thread to handle command
    #try:
    worker = threading.Thread(target=CommandConnection, args=(dataConnection, command))
    worker.start()
    #except:
        #print "Error!"
    worker.join()

#Create socket
mainSock = socket.socket()
host = socket.gethostname()
port = 2000
mainSock.bind((host, port))
mainSock.listen(1)
if __name__ == '__main__':
    while True:
        print 'Waiting for connection'
        #Accept connection
        connection, addr = mainSock.accept()
        print 'Accepting connection'
            
        #Create eph port number
        ephPort = 3000
        #Child listens on eph port
        commandSock = socket.socket()
        commandSock.bind((host, ephPort))
        print 'Child port bound'
        commandSock.listen(5)
        
        #send port number
        connection.send(str(ephPort))
        ephPort += 1

        print 'Child waiting for connection'
        #Accept connection
        dataConnection, addr = commandSock.accept()
        print 'Child accepting connection'

        print 'Creating process'
        #Fork child
        child = multiprocessing.Process(target=ClientConnection, args=(dataConnection,addr,))
        #child.deamon = True
        print 'Starting process'
        child.start()
        dataConnection.send('polo')
        #wait()
