import sys
import socket
import threading
import os
import time
import struct

def log(m):
    print(name + ": " + str(m))


def fileServer(p,fileName):
    fileServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fileServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    fileServerSocket.bind(('',p))
    fileServerSocket.listen(5)
    soc, addr = fileServerSocket.accept()
    fileSaver(soc,fileName)
    fileServerSocket.close()


def fileSender(portReq,fileName):
    socketReq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketReq.connect(('localhost',int(portReq)))
    sockFileSender(socketReq,fileName)
    

def recieveMessage(senderMessage):
    while True:
        try:
            message = senderMessage.recv(1024).decode()
            if message == 'f':
                portReq = senderMessage.recv(1024).decode()
                fileName = senderMessage.recv(1024).decode()
                fileSenderThread = threading.Thread(target=fileSender,args=(portReq,fileName))
                fileSenderThread.start()

            if message == "":
                break
            else:
                print(message)
        except Exception as e:
            break


def control(s, p):
    while True:
        print("Enter an option ('m', 'f', 'x'): ")
        print("(M)essae (send)")
        print("(F)ile (request)")
        print("e(X)it")
        userInput = input()

        if userInput == 'm':
            print("Enter your message:")
            message = 'm' + sys.stdin.readline().rstrip()
            s.send(message.encode())

        if userInput == 'f':
            print("Who owns the file?")
            owner = sys.stdin.readline().rstrip()
            print("Which file do you want?")
            fileName = sys.stdin.readline().rstrip()
            fileServerThread = threading.Thread(target=fileServer,args=(p,fileName))
            fileServerThread.start()
            freq = 'f' + u'\u0394' + owner + u'\u0394' + fileName
            s.send(freq.encode())

        if userInput == 'x':
            log('exiting')
            os._exit(0)

def fileSaver(sock,filename):
    fileSize= sock.recv(4)
    if fileSize:
        file_size= struct.unpack('!L', fileSize[:4])[0]
        if file_size:
            receiveFile(sock, filename)
        else:
            print('File does not exist or is empty')
    else:
        print('File does not exist or is empty')
    sock.close()

def receiveFile(sock, filename):
	file= open(filename, 'wb')
	while True:
		fileBytes= sock.recv(1024)
		if fileBytes:
			file.write(fileBytes)
		else:
			break
	file.close()

def sockFileSender(sock,fileName):
    try:
        file_stat= os.stat(fileName)
        if file_stat.st_size:
            file= open(fileName, 'rb')
            sendFile(sock, file_stat.st_size, file)
        else:
            noFile(sock)
    except OSError:
        noFile(sock)
    sock.close()

def sendFile(sock, file_size, file):
	fileSize= struct.pack('!L', file_size)
	sock.send(fileSize)
	while True:
		fileBytes= file.read(1024)
		if fileBytes:
			sock.send(fileBytes)
		else:
			break
	file.close()

def noFile( sock ):
	noBytes= struct.pack( '!L', 0 )
	sock.send( noBytes )

listenPort = int(sys.argv[2])
serverPort = int(sys.argv[4])

if len(sys.argv) > 5:
    global name
    name = str(sys.argv[5])
else:
    print("What is your name?")
    name = sys.stdin.readline()

senderMessage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
senderMessage.connect(('localhost',serverPort))

senderMessage.send(name.encode())
time.sleep(0.5)
senderMessage.send(str(listenPort).encode())

recieveThread = threading.Thread(target=recieveMessage, args=(senderMessage,))
recieveThread.start()

control(senderMessage, listenPort)



