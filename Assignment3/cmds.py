# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************
import commands
import os

MAX_LENGTH_SIZE = 10

class FTP_COMMANDS:

	__server_commands = ["ls", "get", "cd", "mkdir", "quit", "remove"]
	__client_commands = ["put"]
	__list_of_valid_commands = __server_commands + __client_commands

	#Initializing the class for FTP
	def __init__(self, cmd = None, amIServer = False):

		#Checking to if command was implemented
		if isinstance(cmd, basestring):
			self.command_args = cmd.split()
			self.isCommand = self.CheckCommand()
		elif isinstance(cmd, list):
			self.command_args = cmd
			self.isCommand = self.CheckCommand()
		else:
			self.command_args = None
			self.isCommand = False

		self.amIServer = amIServer

	#Check to see if it is a command we created or will implement                
	def CheckCommand(self):
		if self.command_args != None:
			if self.command_args[0]  in self.__list_of_valid_commands:
				return True
			else:
				return False
		else:
			return False
					
	#Check whether to run the command in the server                
	def CommandDoneInServer(self, cmd):
		if self.commands_args != None:
			if cmd in self.__server_commands:
				return True
			else:
				return False
		else:
			 return False

	#Check whether to run the command in the client
	def CommandDoneInClient(self, cmd):
		if self.commands_args != None:
			if cmd in self.__client_commands:
				return True
			else:
				return False
		else:
			 return False

	#Even return command string and size
	def GetCommandInfo(self):
		if self.isCommand:
			return ( ' '.join(self.command_args), len(' '.join(self.command_args)))
		else:
			return (None, 0)

	def NewCommand(self, newCmd):
		if isinstance(newCmd, basestring):
			self.command_args = newCmd.split()
			self.isCommand = self.CheckCommand(self.command_args[0])
					
		elif isinstance(newCmd, list):
			self.command_args = newCmd
			self.isCommand = self.CheckCommand(self.command_args[0])
					
		else:
			self.command_args = None
			self.isCommand = False
	
	def RunCommand(self, commandSocket):
		if self.isCommand:
			dataBuffer = ""
			length = 0
			recBuffer = ""
			if self.amIServer:
				#Run Each Command for Server
				if self.command_args[0] == "ls":
					dataBuffer, length = GetListInDirectory(GetCommandInfo[0])
					SendData(dataBuffer, length, commandSocket)
						
				elif self.command_args[0] == "get":
					dataBuffer, length = FindFile(GetCommandInfo[1], ".")
					SendData(dataBuffer, length, commandSocket)
						
				elif self.command_args[0] == "quit":
					commandSocket.close()
						
				elif self.command_args[0] == "put":
					refBuffer = ReceiveData(commandSocket)
					fo = open(GetCommandInfo[1], "w+")
					fo.write(recBuffer)
					fo.close()
			else:
				#Run Each Command for Client
				if self.command_args[0] == "ls":
					recBuffer = ReceiveData(commandSocket)
					print recBuffer
						
				elif self.command_args[0] == "get":
					recBuffer = ReceiveData(commandSocket)
					fo = open(GetCommandInfo[1], "w+")
					fo.write(recBuffer)
					fo.close()
						
				elif self.command_args[0] == "quit":
					commandSocket.close()
						
				elif self.command_args[0] == "put":
					dataBuffer, length =  FindFile(GetCommandInfo[1], ".")
					SendData(dataBuffer, length, commandSocket)

			self.command_args = None
			self.isCommand = False

									
	def recvAll(sock, numBytes):
		# The buffer
		recvBuff = ""
		
		# The temporary buffer
		tmpBuff = ""
		
		# Keep receiving till all is received
		while len(recvBuff) < numBytes:
			
			# Attempt to receive bytes
			tmpBuff =  sock.recv(numBytes)
			
			# The other side has closed the socket
			if not tmpBuff:
					break
			
			# Add the received bytes to the buffer
			recvBuff += tmpBuff
		
		return recvBuff

							
	def ReceiveData(self, commandSocket):

		###################### Send Temp Port ###################### 
		# Create a socket
		tempDataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Bind the socket to port 0
		tempDataSocket.bind(('',0))

		# int value of port
		tempPortData = tempDataSocket.getsockname()[1]

		# how many sockets is it waiting for, which is one
		tempPortData.listen(1)
		
		# get string of the length
		tempPortDataStr = str(len(tempPortData))

		# Prepend 0's to the size string
		# until the size is 10 bytes
		while len(tempPortDataStr) < MAX_LENGTH_SIZE:
			tempPortDataStr = "0" + tempPortDataStr

		# Prepend the size of the data to the
		# file data.
		tempPortDataStr = tempPortDataStr + str(temPortData)       

			# The number of bytes sent
		numSent = 0
			
		while len(tempPortDataStr) > numSent:
			numSent += commandSocket.send(tempPortDataStr[numSent:])

		####################### Receive DataBuffer #######################

		dataSizeBuff = ""
		dataSizeBuff = recAll(tempDataSocket, 10)
		dataNumSize = 0
		dataNumSize = int(dataSizeBuff)

		dataBuffer = (tempDataSocket, dataNumSize)

		tempDataSocket.close()
		
		return dataBuffer
	
	#Sending data similar to the assignment sample code given
	def SendData(self, dataBuffer, length, commandSocket):

		###################### Receive Temp Port ###################### 
		tempDataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# The size of the incoming port number
		portNumSize = 0	
		
		# The buffer containing the file size
		portSizeBuff = ""
		
		# Receive the first 10 bytes indicating the
		# size of the port
		portSizeBuff = recvAll(commandSocket, 10)
				
		# Get the port size
		portNumSize = int(portSizeBuff)
		
		# Get the port number
		serverTempPort = int( recvAll(commandSocket, portNumSize) )

		tempDataSocket.connect( commandSocket.getsockname()[0], serverTempPort )

		dataSizeStr = str(length)


		####################### Send DataBuffer #######################
		# Prepend 0's to the size string
		# until the size is 10 bytes
		while len(dataSizeStr) < MAX_LENGTH_SIZE:
			dataSizeStr = "0" + dataSizeStr


		# Prepend the size of the data to the
		# file data.
		dataBuffer = dataSizeStr + dataBuffer	
		
		# The number of bytes sent
		numSent = 0

		while len(dataBuffer) > numSent:
			numSent += self.dataSocket.send(dataBuffer[numSent:])

		tempDataSocket.close()

	def FindFile(name, path):
		for root, dirs, files in os.walk(path):
			if name in files:
				file_name = os.path.join(root, name)
				return (file_name, len(file_name))
			else:
				response = "File does not exist"
				return (response, len(response))

	def GetListInDirectory(cmd):

		dataBuffer = ""
		
		for line in commands.getstatusoutput(GetCommandInfo[0]):
				if isinstance(line, basestring):
						dataBuffer += line

		return (dataBuffer, len(dataBuffer))
			


