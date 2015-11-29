__author__ = 'Alexander Mark, FireVPN'

import sys
import socket
import time
import threading
import pickle

""""
Parameter nach dem File (zB.: python3 server.py 10.0.0.1 8888)
sys.argv[1] private IP des Hosts (zB.: 10.0.0.1)
sys.argv[2] Port des Hosts (zB.: 8888)
"""""

class Server():

    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind((sys.argv[1], int(sys.argv[2])))
        print ("set up port on ", sys.argv[1], sys.argv[2])
        self.sock.listen(5)
        print ("Socket set to listen")
        self.addr=list()

    def accept_connection(self):
        while True:
            clientsocket =self.sock.accept()
            print ("Got new Connection")
            threading.Thread(target=self.receive, args=[clientsocket]).start()


    def receive(self, clientsocket):
        print("started new Thread")
        while True:
            if clientsocket[1] not in self.addr:
                self.addr.append(clientsocket[1])
                print ("Added:", clientsocket[1])
            data=clientsocket[0].recv(1024)

            if (data.decode('utf-8')=="R"):
                clientsocket[0].send(pickle.dumps(self.addr))
                print("send back list to", clientsocket[1])


def main():
    srv=Server()
    srv.accept_connection()

if __name__ == '__main__':
    main()
