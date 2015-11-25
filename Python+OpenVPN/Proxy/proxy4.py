__author__ = 'Elias Eckenfellner'
import threading, socket

class Proxy:

    def __init__(self, ip, port):
        self.SERVER=False
        LOCALVPNPORT=0
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        print("Binded to ", ip, ":", port)

    def recv(self):
        print("Recieving")
        data, addr = self.sock.recvfrom(4096)
        if not self.SERVER:
            LOCALVPNPORT=addr[1]
            #Kill den anderen recv[intern/extern]
        print("int to ext")

    def send(self):
        print("sending")


def main():
    global externrecv
    global internrecv
    intern=Proxy("127.0.0.1", 6220, externrecv)
    extern=Proxy("10.0.0.1", 6221, internrecv)
    recvintern=threading.Thread(target=intern.recv).start()
    recvextern=threading.Thread(target=extern.recv).start()

if __name__ == '__main__':
    main()