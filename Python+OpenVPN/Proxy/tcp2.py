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
           print("Verbindung zu VPN hergestellt")
           self.ext_sock.connect(PEER)
           print("Verbindung zu PEER hergestellt")
           proxy_extern = Proxy(connint.dup(), self.ext_sock.dup())
       else:
           self.int_sock.connect(LOCALVPN)
           print("Verbindung zu VPN hergestellt")
           self.ext_sock.listen(5)
           connext, addr = self.ext_sock.accept()
           print("Verbindung zu PEER hergestellt")
           proxy_intern = Proxy(self.int_sock.dup(), connext.dup())
       tintern = threading.Thread(target=Proxy.intern)
       textern = threading.Thread(target=Proxy.extern)
       while True:
           print("vor weiter")
           dataint = tintern.start()
           print("WEITER")
           dataext = textern.start()


class Proxy:
    def __init__(self, int_sock, ext_sock):
       self.int_sock = int_sock
       self.ext_sock = ext_sock

    def intern(self):
        while True:
           data = self.int_sock.recv(4096)
           return data
    def extern(self):
        return None

def main():
   init = Init()
if __name__ == '__main__':
   main()