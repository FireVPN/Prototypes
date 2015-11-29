__author__ = 'Alexander Mark, FireVPN'

import sys
import socket
import time

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

    def accept_connection(self):
        clientsocket =self.sock.accept()
        print ("Got new Connection")
        return True, clientsocket


def main():
    srv=Server()
    while (True):
        connection, clientsocket=srv.accept_connection()
        if (connection):
            #neuer Thread
            print ("lala")
        else:
            time.sleep(10)


if __name__ == '__main__':
    main()
