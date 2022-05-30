# source: https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/

import socket

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 65433 # même port que chez le serveur
print('Waiting for connection response')


try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)

while True:
    Input = input('Choix d\'action : ')
    ClientMultiSocket.send(str.encode(Input)) # ce que le client envoit au serveur
    res = ClientMultiSocket.recv(1024) # ce que le client reçoit du serveur
    print(res.decode('utf-8'))

ClientMultiSocket.close()