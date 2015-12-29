__author__ = 'Elias Eckenfeller'
import sys, socket, threading, platform
SERVER=True
PEER=("10.0.0.2", 6222)
EXT=("10.0.0.1", 6222)
localvpnport=0
LOCALVPN=("localhost", 6220)
INT=("localhost", 6221)

class Init():
    def __init__(self):
        print("Starting Proxy")
        self.ext_sock = socket.socket()
        self.ext_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if("Windows" not in platform.platform()):
            self.ext_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.ext_sock.bind(EXT)
        self.int_sock = socket.socket()
        self.int_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if("Windows" not in platform.platform()):
            self.int_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.int_sock.bind(INT)
        if(not SERVER):
            self.int_sock.listen(5)
            connint, addr = self.int_sock.accept()
            localvpnport=addr[1]
            self.ext_sock.connect(PEER)
            proxy_intern = Proxy_intern(connint, self.ext_sock)
            proxy_extern = Proxy_extern(connint, self.ext_sock)
        else:
            self.int_sock.connect(LOCALVPN)
            self.ext_sock.listen(5)
            connext, addr = self.ext_sock.accept()
            proxy_intern = Proxy_intern(self.int_sock, connext)
            proxy_extern = Proxy_extern(self.int_sock, connext)
        tintern = threading.Thread(target=proxy_intern.run())
        textern = threading.Thread(target=proxy_extern.run())
        tintern.start()
        textern.start()

class Proxy_intern():
    def __init__(self, int_sock, ext_sock):
        self.int_sock = int_sock
        self.ext_sock = ext_sock
    def run(self):
        while True:
            data = self.int_sock.recv(1024)
            self.ext_sock.send(data)

class Proxy_extern():
    def __init__(self, int_sock, ext_sock):
        self.int_sock = int_sock
        self.ext_sock = ext_sock
    def run(self):
        while True:
            data = self.ext_sock.recv(1024)
            self.int_sock.send(data)

def main():
    init = Init()
if __name__ == '__main__':
    main()