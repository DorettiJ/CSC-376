import os
import threading

global clist 
clist = []

class clientReceiver (threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self) 
		self.sock = sock 
		
	def run(self):
		msg = self.sock.recv(1024)
		while True:
			print (msg.decode())
			msg = self.sock.recv(1024)
		os._exit(0)

class serverReceiver (threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.sock = sock

	def run(self):
		name = self.sock.recv(1024).decode()
		msg = self.sock.recv(1024)
		while msg: 
			message = name + ": " + msg.decode()
			for client in clist: 
				if client != self.sock: 
					client.send(message.encode()) 
			msg = self.sock.recv(1024) 
		clist.remove(self.sock) 