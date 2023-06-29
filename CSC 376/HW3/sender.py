import sys
import os 
import threading

class sender (threading.Thread): 
	def __init__(self, sock, message):
		threading.Thread.__init__(self) 
		self.sock = sock 
		self.message = message 
		
	def run(self):
		while self.message: 
			self.sock.send(self.message.encode()) 
			self.message = sys.stdin.readline().replace("\n", "")
		os._exit(0)