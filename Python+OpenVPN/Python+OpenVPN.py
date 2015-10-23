__author__ = 'Elias Eckenfellner'
import time, sys
IP="192.168.0.1"
PORT="90"

class Client():
    def __init__(self, ip):
        self.send()
    def send(self):
        ip = self.variable.get()
        port = None
        try:
            self.sock.sendto(self.text.get().encode('utf-8'), (IP, PORT))
            time.sleep(1)
        except:
            print ("Open UDP Socket")
            sys.exit(1)

def main():
    client = Client()

if __name__ == '__main__':
    main()