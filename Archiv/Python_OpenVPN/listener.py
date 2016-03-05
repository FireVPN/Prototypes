import sys, socket
IP="127.0.0.1"
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
            data, addr = self.sock.recvfrom(1024)
            utf_data = data.decode('utf-8')
            print(utf_data)

def main():
    listener = Listener()

if __name__ == '__main__':
    main()