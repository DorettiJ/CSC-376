import sys 
import socket 
import sender
import receiver


args = sys.argv
port = int(args[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('localhost', port))
print("Enter name: ")
name = sys.stdin.readline().replace("\n", "")

receiveT = receiver.clientReceiver(sock) 
sendT = sender.sender(sock, name)
receiveT.start()
sendT.start()