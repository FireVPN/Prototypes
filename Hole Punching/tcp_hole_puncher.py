__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter
# sys.argv[1] == IP Addresse (destination)
# sys.argv[3] == Source Port
# sys.argv[2] == Destination Port

import sys
import socket
import _thread as thread

def client():
    client_socket = socket.socket()

    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    #c.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))
    client_socket.bind('', int(sys.argv[3]))
    while(client_socket.connect_ex((sys.argv[1], int(sys.argv[2])))):
        pass
    print("connected!")
    thread.interrupt_main()

def server():
    srv_socket = socket.socket()

    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    #c.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))
    srv_socket.bind('', int(sys.argv[3]))
    srv_socket.listen(5)
    srv_socket.accept()
    print("connected!")
    thread.interrupt_main()

def main():
    thread.start_new_thread(client, ())
    thread.start_new_thread(server, ())

    while True:
        pass

if __name__ == '__main__':
    main()

