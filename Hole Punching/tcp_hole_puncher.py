__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter

import sys
import socket
import _thread as thread

def client():
    c = socket.socket()

    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    c.bind('', int(sys.argv[3]))
    while(c.connect_ex((sys.argv[1], int(sys.argv[2])))):
        pass
    print("connected!")
    thread.interrupt_main()

def server():
    c = socket.socket()

    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    c.bind('', int(sys.argv[3]))
    c.listen(5)
    c.accept()
    print("connected!")
    thread.interrupt_main()

def main():
    thread.start_new_thread(client, ())
    thread.start_new_thread(server, ())

    while True:
        pass

if __name__ == '__main__':
    main()

