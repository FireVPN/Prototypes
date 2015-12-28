import socket, sys, pickle, threading, time

SERV_IP = "0.0.0.0"
SERV_PORT = 45678
loginsToServer = set()
names = set()
heartbeats = set()
connections = set()


class Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((SERV_IP, SERV_PORT))
            self.sock.settimeout(1)
        except:
            print ("Could not set up socket.")
            sys.exit(1)


    def run(self):
        while not self.event.is_set():
            try:
                data, addr = self.sock.recvfrom(1024)
            except:
                continue
            host = addr[0]
            port = addr[1]
            receivedData = data.decode('utf-8').split(';')
            indicator = receivedData[0]
            name = None
            print ("NEW MESSAGE")
            print (host)
            print (loginsToServer)
            for l in loginsToServer:
                if host == l[1] and port == l[2]:
                    name = l[0]


            # more tests needed?
            #if not receivedData[0] == "H" and not receivedData[0] == "E" and not receivedData[0] == "X" and not receivedData[0] == "Y":
            if indicator == "M":
                print (name)
                print (connections)
                for c in connections:
                    if name == c[0]:
                        for l in loginsToServer:
                            #print ("1")
                            if l[0] == c[1]:
                                self.sock.sendto(data, (l[1], l[2]))
                                continue
                    elif name == c[1]:
                        for l in loginsToServer:
                            #print ("2")
                            if l[0] == c[0]:
                                self.sock.sendto(data, (l[1], l[2]))
                                continue

            elif indicator is 'L':
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
                        print (receivedData[1]+"_(2) tried to connect. Nickname was already present.")
                    except:
                        sys.exit(1)

            elif indicator is 'H':
                print ("Heartbeat received from: " + host, port)
                for c in loginsToServer:
                    if (host, port) == (c[1], c[2]):
                        name = c[0]
                for h in heartbeats:
                    if name == h[0]:
                        heartbeats.discard(h)
                        break
                heartbeats.add((name, time.time()))

            elif indicator is 'E':
                for n in loginsToServer:
                    if n[0] == receivedData[1]:
                        discard = (receivedData[1], host, port)
                        if discard in loginsToServer:
                            loginsToServer.discard(discard)
                            names.discard(receivedData[1])
                            for h in heartbeats:
                                if h[0] == discard[0]:
                                    hDiscard = h
                            heartbeats.discard(hDiscard)
                            print (discard[0], "closed the connection.")
                        self.broadcast(names)
                        break

            elif indicator is 'C':
                print (receivedData[1], " wants to connect to ", receivedData[2])
                for c in loginsToServer:
                    if c[0] == receivedData[2]:
                        connections.add((receivedData[1], None, False))
                        self.sock.sendto(('C'+';'+(pickle.dumps(c).decode('ISO-8859-1'))).encode(),(host, port))
                        self.sock.sendto(('Q'+';'+(pickle.dumps((receivedData[1], host, port)).decode('ISO-8859-1'))).encode(),(c[1], c[2]))

            elif indicator is 'Y':
                print (receivedData[1], " agrees to ", receivedData[2])
                for connection in connections:
                    if connection[0] == receivedData[2]:
                        connections.remove(connection)
                        connection = (receivedData[2], receivedData[1], False)
                        connections.add(connection)
                        for c in loginsToServer:
                            if c[0] == receivedData[1] or c[0] == receivedData[2]:
                                self.giveStart(c)

            elif indicator is 'X':
                #print ("received X ", receivedData[1])
                for connection in connections:
                    if connection[0] == receivedData[1]:
                        if connection[2]:
                            continue
                        new_connection = (receivedData[1], connection[1], True)
                        connections.remove(connection)
                        connections.add(new_connection)
                        print (new_connection, " over server")
                        for l in loginsToServer:
                            print (l)
                            if new_connection[0] == l[0]:
                                #print ("send x to ", (l[1], l[2]))
                                self.sock.sendto(("X"+";").encode(), (l[1], l[2]))
                            elif new_connection[1] == l[0]:
                                #print ("send x to ", (l[1], l[2]))
                                self.sock.sendto(("X"+";").encode(), (l[1], l[2]))


    def giveStart(self, c):
        self.sock.sendto(("S"+";").encode(), (c[1], c[2]))

    def broadcast(self, obj):
        cache = obj.copy()
        try:
            for c in loginsToServer:
                cache.discard(c[0])
                self.sock.sendto(('R'+';'+(pickle.dumps(cache).decode('ISO-8859-1'))).encode(),(c[1],c[2]))
                cache = obj.copy()
        except:
            print ("Could not send broadcast.")

    def stop(self):
        self.event.set()

class HeartbeatController(threading.Thread):
    def __init__(self, receiver):
        threading.Thread.__init__(self)
        self.receiver = receiver
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            for h in heartbeats:
                if (time.time()-h[1] > 15):
                    heartbeats.discard(h)
                    names.discard(h[0])
                    for c in loginsToServer:
                        if c[0] == h[0]:
                            loginsToServer.discard(c)
                            break
                    self.receiver.broadcast(names)
                    print ("someone left.")
                    break
            self.event.wait(15)

def main():
    rec = Receiver()
    hrb = HeartbeatController(rec)
    try:
        rec.start()
        hrb.start()
    except KeyboardInterrupt:
        rec.stop()
        hrb.stop()

if __name__ == '__main__':
    main()
