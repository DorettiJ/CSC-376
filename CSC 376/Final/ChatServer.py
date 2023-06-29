import sys
import socket
import threading
import time

def sendReciever(cs):
    clientName = cs.recv(1024).decode().rstrip()
    clients[cs][0] = clientName
    clientPort = cs.recv(1024).decode().rstrip()
    clients[cs][1] = (clientPort)
 
    while True:
        try:
            message = cs.recv(1024).decode()
            if message[0] == 'f':
                
                freq = message.rsplit(u'\u0394')
                fileOwner = freq[1]
                fname = freq[2]
        
                for sock in clients:
                    if clients[sock][0] == fileOwner:
                        
                        sock.send(('f').encode())
                        time.sleep(0.1)
                        sock.send((clients[cs][1]).encode())
                        time.sleep(0.1)
                        sock.send(fname.encode())

            if message[0] == 'm':
                for sock in clients:
                    if sock != cs:
                        sock.send((clients[cs][0] + ": "+ message[1:]).encode())
        except Exception as e:
            clients.pop(cs)
            break

def listen(server):
    while True:
        sock, addr = server.accept()
        clients[sock] = ['',0]
        sendRecieverThread = threading.Thread(target=sendReciever,args=(sock,))
        sendRecieverThread.start()

listenPort = int(sys.argv[1])

global clients
clients = {}

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #returns socket object 'serversocket'

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

serverSocket.bind(('', listenPort))

serverSocket.listen(5)

listen(serverSocket)