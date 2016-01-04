import socket, sys, pickle, threading

SERV_IP = "0.0.0.0"
SERV_PORT = 45678
loginsToServer = set()
names = set()
connections = set()


class Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        print ("starting programm")

        #try:
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden
        self.sock.bind((SERV_IP, SERV_PORT))
            #self.sock.settimeout(1)
        self.sock.listen(5)
        #except:
        #    print ("Could not set up socket.")
        #    sys.exit(1)

        print ("socket set up")
        while True:
            print("waiting for new connections")
            clientsocket=self.sock.accept()
            threading.Thread(target=self.run, args=[clientsocket]).start() #neuen Tread starten (run methode und clientsocket als parameter)


    def run(self, clientsocket):
        while True:
            try:
                conn_sock, addr = clientsocket
                data = conn_sock.recv(1024)
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
                        loginsToServer.add((receivedData[1], host, port, conn_sock))
                        names.clear()
                        for n in loginsToServer:
                            names.add(n[0])
                            print (receivedData[1], "joined.")
                            self.broadcast(names)
                    else:
                        try:
                            conn_sock.send(('N'+';'+'Nickname is already present').encode('utf-8'))
                            print (receivedData[1]+"_(2) tried to connect. Nickname was already present.")
                        except:
                            sys.exit(1)

                elif indicator is 'E':
                    to_remove=None
                    for l in loginsToServer:
                        if host == l[1] and port == l[2]:
                            to_remove=l
                    to_remove[3].close()
                    loginsToServer.remove(to_remove)
                    self.sock.close()
                    conn_sock.close()
                    print ("closed connection")
                    break

                elif indicator is 'C':
                    print (receivedData[1], " wants to connect to ", receivedData[2])
                    for c in loginsToServer:
                        if c[0] == receivedData[2]:
                            connections.add((receivedData[1], None, False))
                            conn_sock.send(('C'+';'+(pickle.dumps((c[0], c[1], c[2])).decode('ISO-8859-1'))).encode())
                            c[3].send(('Q'+';'+(pickle.dumps((receivedData[1], host, port)).decode('ISO-8859-1'))).encode())

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

            except ConnectionRefusedError:
                # connection refused
                to_remove=None
                for l in loginsToServer:
                    if host == l[1] and port == l[2]:
                        to_remove=l
                to_remove[3].close()
                loginsToServer.remove(to_remove)
                self.sock.close()
                conn_sock.close()
                print ("closed connection")
                break



    def giveStart(self, c):
        c[3].send(("S"+";").encode())

    def broadcast(self, obj):
        cache = obj.copy()
        try:
            for c in loginsToServer:
                cache.discard(c[0])
                c[3].send(('R'+';'+(pickle.dumps(cache).decode('ISO-8859-1'))).encode())
                cache = obj.copy()
        except:
            print ("Could not send broadcast.")

    def stop(self):
        self.event.set()



def main():
    rec = Receiver()
    try:
        rec.start()
    except KeyboardInterrupt:
        rec.stop()

if __name__ == '__main__':
    main()
