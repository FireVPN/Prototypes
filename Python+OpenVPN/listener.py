__author__ = 'Owner'
import sys, socket
IP="192.168.0.9"
PORT=6222

class Listener():
    def __init__(self):
        self.recieve()
    def recieve(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((IP, PORT))
        except:
            print ("UDP-Socket konnte nicht geöffnet werden!")
            sys.exit(1)
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                utf_data = data.decode('utf-8')
                print(utf_data)
            except:
                print ("Es konnte nicht über den UDP-Socket empfangen werden!")
                sys.exit(1)

def main():
    listener = Listener()

if __name__ == '__main__':
    main()