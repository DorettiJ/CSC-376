import sys
import socket
import receiver

args = sys.argv 
port = int(args[1]) 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serversocket.bind(('', port))
serversocket.listen(5) 


while (True): 
	sock, addr = serversocket.accept() 
	receiver.serverReceiver(sock).start() 
	receiver.clist.append(sock)