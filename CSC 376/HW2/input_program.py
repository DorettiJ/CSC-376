#import statements
import sys 
import socket
import os
import threading

#class declaratiosn
class receiver (threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self) 
		self.sock = sock 
		
	#Wait for messages until enter is hit
	def run(self):
		msg = self.sock.recv(1024)
		while True:
			print (msg.decode())
			msg = self.sock.recv(1024)
		os._exit(0)

class sender (threading.Thread): 
	def __init__(self, sock, message):
		threading.Thread.__init__(self) 
		self.sock = sock 
		self.message = message 
		
	#Wait for messages until enter is hit
	def run(self):
		while self.message: 
			self.sock.send(self.message.encode()) 
			self.message = sys.stdin.readline().replace("\n", "")
		os._exit(0)

def createThread(sock):
    receiveThread = receiver(sock)
    receiveThread.start() #starts thread

    message = sys.stdin.readline().replace("\n", "") #Saves user input

    sendThread = sender(sock, message)
    sendThread.start()

#Function defenitions
def server (port):
	servs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initializes socket
	servs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows multiple sockets
	servs.bind(('', port)) # Binds servs & port
	servs.listen(5) # Listens for socket connections
	sock, addr = servs.accept() #Accept connection
	servs.close() #close ss
	createThread(sock)


def client (port): 
	cls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cls.connect(('localhost', port)) #Connects to server
	createThread(cls)

def commandLine():
	args = sys.argv 
	if len(args) == 2: # 2 cmdline args is client
		port = int(args[1])
		client(port)
	elif len(args) == 3: # 3 cmdline args is server
		port = int(args[2])
		server(port)
	else: 
		sys.exit()

commandLine()