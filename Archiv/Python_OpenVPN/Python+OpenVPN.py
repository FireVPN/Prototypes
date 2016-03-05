import time, sys, socket
IP="192.168.0.9"
PORT=6222

class Client():
    def __init__(self):
        self.send()
    def send(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("UDP-Socket konnte nicht geöffnet werden!")
            sys.exit(1)
        try:
            sock.sendto("Hier wird über den UDP-Socket gesendet!".encode('utf-8'), (IP, PORT))
            time.sleep(1)
        except:
            print ("Über den UDP-Socket konnte nichts gesendet werden!")
            sys.exit(1)
        print ("Socket steht und es wurde schon darüber übertragen")
        time.sleep(20)

def main():
    client = Client()

if __name__ == '__main__':
    main()