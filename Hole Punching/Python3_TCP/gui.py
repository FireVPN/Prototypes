__author__ = 'Alexander Mark, FireVPN'

import sys
import socket
import pickle
import threading as thread
#import _thread as thread
from PyQt4 import QtGui, QtCore



class Client(QtGui.QWidget):
    logins=set()
    ip=sys.argv[1]
    port =int(sys.argv[3])


    def __init__(self):
        super(Client, self).__init__()

        self.initUI()

    #GUI
    def initUI(self):

        #connect to server button erstellen
        qbtn_connect_srv = QtGui.QPushButton('Connect to Server', self)
        QtGui.QWidget.connect(qbtn_connect_srv, QtCore.SIGNAL("clicked()"), self.init_srv_connct)
        #qbtn_connect_srv.clicked.connect(thread.start_new_thread(Controller.connect_to_server(self)))
        #QtGui.QWidget.connect(qbtn_connect_srv, QtCore.SIGNAL("clicked()"), thread.Thread(self.connect_to_server()).start())
        qbtn_connect_srv.resize(qbtn_connect_srv.sizeHint())

        #combobox erstellen
        address_box=QtGui.QComboBox(self)
        address_box.addItem("IP : Port")
        address_box.resize(address_box.sizeHint())
        address_box.move(0, 30)
        self.address_box=address_box

        #connect to client button erstellen
        qbtn_connect_client = QtGui.QPushButton('Connect to Client', self)
        QtGui.QWidget.connect(qbtn_connect_client, QtCore.SIGNAL("clicked()"), self.init_client_connect)
        #qbtn_connect_client.clicked.connect(Controller.foo(self))
        qbtn_connect_client.resize(qbtn_connect_client.sizeHint())
        qbtn_connect_client.move(100, 30)

        #quit button erstellen
        qbtn_quit = QtGui.QPushButton('Quit', self)
        qbtn_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn_quit.resize(qbtn_quit.sizeHint())
        qbtn_quit.move(0, 60)

        #launch
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('TCP Hole-Puncher')
        self.show()
        #qbtn_connect_srv.clicked.connect(self.connect_to_server())

    #verbindung zu server initieren
    def init_srv_connct(self):
        t1=thread.Thread(target=self.connect_to_server())
        t1.start()

    #connect to client initieren
    def init_client_connect(self):
        ip=""
        port=0

        entry=self.address_box.activated[str](self)
        ip=entry.split(":")[0]
        port=int(entry.spilt(":")[1])

        t1=thread.Thread(target=self.connect_to_client(ip, port))
        t2=thread.Thread(target=self.listen())
        t1.start()
        t2.start()


    #sendet syn Packete aus waehrend des hole punching prozesses
    def connect_to_client(dest_ip,dest_port,self):
        try:
            connect_socket = socket.socket()

            connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
            connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

            connect_socket.bind((self.ip, self.port)) #IP + Port "zusammenfuehren"
            #connect_socket.bind('', int(sys.argv[3])) => nur fuer loopback tests
        except:
            print ("Could not set up socket. (SYN flooding)")
            sys.exit(1)

        while(connect_socket.connect_ex((dest_ip, dest_port))): #SYN packets flooding
            pass
        print("connected!")
        thread.interrupt_main()

    #listen fuer eingehende SYN Packets, waehrend des hole punching prozesses. (Verbindungsannahme)
    def listen(self):
        try:
            listen_socket = socket.socket()

            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

            listen_socket.bind((self.ip, self.port ))#IP + Port "zusammenfuehren"
            #listen_socket.bind('', int(sys.argv[3])) => nur fuer loopback tests
        except:
            print ("Could not set up socket. (Listening)")
            sys.exit(1)

        listen_socket.listen(5) #listen starten, auf das SYN flooding warten
        listen_socket.accept() # Verbindung annehmen
        print("connected!")
        thread.interrupt_main()

    #verbindet sich mit dem Server und Server traegt Addressen ein und sendet seine vorhandenen Addressen zurueck
    def connect_to_server(self):
        try:
            srv_conn_socket = socket.socket()

            srv_conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Addresse wieder verwenden
            srv_conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)#Port wieder verwenden

            srv_conn_socket.bind((self.ip, self.port))#IP + Port "zusammenfuehren"
        except:
            print ("Could not set up socket. (SRV connection)")
            sys.exit(1)
        print("start connecting")
        #srv_conn_socket.bind('', int(sys.argv[3]))
        while(srv_conn_socket.connect_ex((sys.argv[4], int(sys.argv[2])))):#SYN Packets an Server senden
            pass
        print("connected to server!")

        #daten von server bekommen/anfordern/senden
        srv_conn_socket.send(b'LR') #Daten eintragen und liste vom server bekommen
        print ("LR sent")
        #srv_conn_socket.send("R") #Daten vom server holen
        #srv_conn_socket.send("L") #Daten in liste eintragen

        data= srv_conn_socket.recv(1024) #daten von server erhalten
        print ("recived...")
        #utf_data = pickle.load(data)

        self.logins = pickle.loads(data)

        print(self.logins)
        self.update_combo_box()

        #thread.join()

    #combobox aktuallisieren von den ergebnissen des servers
    def update_combo_box(self):
        for i in self.logins:
            self.address_box.addItem(i[0]+":"+str(i[1]))


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Client()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


