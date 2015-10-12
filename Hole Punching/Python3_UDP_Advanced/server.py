import socket, sys, pickle, threading

SERV_IP = "0.0.0.0"
SERV_PORT = 4567
loginsToServer = set()
names = set()

class Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((SERV_IP, SERV_PORT))
        except:
            print ("Could not set up socket.")
            sys.exit(1)

    def run(self):
        while not self.event.is_set():
            data, addr = self.sock.recvfrom(1024)
            host = addr[0]
            port = addr[1]
            receivedData = data.decode('utf-8').split(';')
            indicator = receivedData[0]

            if indicator is 'L':
                s = False
                if receivedData[1] in names:
                    s = True

                if s is False:
                    loginsToServer.add((receivedData[1], host, port))
                    names.clear()
                    for n in loginsToServer:
                        names.add(n[0])
                    print (receivedData[1], "joined.")
                    self.broadcast(names)
                else:
                    try:
                        self.sock.sendto(('N'+';'+'Nickname is already present').encode('utf-8'), (host, port))
                        print (receivedData[1], "_(2) tried to connect. Nickname was already present.")
                    except:
                        sys.exit(1)

            elif indicator is 'R':
                self.sock.sendto(pickle.dumps(names), (host, port))
                print ("sent reload.")

            elif indicator is 'H':
                print ("Heartbeat received from: " + host, port)

            elif indicator is 'E':
                for n in loginsToServer:
                    if n[0] == receivedData[1]:
                        discard = (receivedData[1], host, port)
                        if discard in loginsToServer:
                            loginsToServer.discard(discard)
                            names.discard(receivedData[1])
                            print (discard[0], "closed the connection.")
                        self.broadcast(names)
                        break

    def broadcast(self, obj):
        #try:
        for c in loginsToServer:
            self.sock.sendto(('R'+';'+(pickle.dumps(obj).decode('ISO-8859-1'))).encode(),(c[1],c[2]))
        #except:
            #print ("Could not send broadcast.")

    def stop(self):
        self.event.set()

class HeartbeatController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.Event = threading.Event




def main():
    rec = Receiver()
    try:
        rec.start()
    except KeyboardInterrupt:
        rec.stop()

if __name__ == '__main__':
    main()
