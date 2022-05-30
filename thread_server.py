# source: https://www.positronx.io/create-socket-server-with-multiple-clients-in-python/

import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 65433 # même port que chez le client
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048) # reception de l'input des clients
        decoded = data.decode('utf-8')
        
        if not data:
            break

        elif int(decoded) == 1:
            response = "Vous avez choisi d'attaquer."
        elif int(decoded) == 2:
            response = "Vous avez choisi de changer de pokemon."
        elif int(decoded) == 3:
            response = "Vous avez choisi de prendre la fuite."

        connection.sendall(str.encode(response)) # envoye la réponse aux clients
    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()


