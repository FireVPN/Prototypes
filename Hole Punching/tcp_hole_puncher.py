__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter
# sys.argv[1] == IP Addresse (source)
# sys.argv[3] == Source Port
# sys.argv[2] == Destination Port (server)
# sys.argv[4] == Destination IP (server)


import sys
import socket
import pickle
import _thread as thread

#sendet syn Packete aus waehrend des hole punching prozesses
def connect(dest_ip,dest_port):
    try:
        connect_socket = socket.socket()

        connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
        connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

        connect_socket.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3]))) #IP + Port "zusammenfuehren"
        #connect_socket.bind('', int(sys.argv[3])) => nur fuer loopback tests
    except:
        print ("Could not set up socket. (SYN flooding)")
        sys.exit(1)

    while(connect_socket.connect_ex((dest_ip, dest_port))): #SYN packets flooding
        pass
    print("connected!")
    thread.interrupt_main()

#listen fuer eingehende SYN Packets, waehrend des hole punching prozesses. (Verbindungsannahme)
def listen():
    try:
        listen_socket = socket.socket()

        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

        listen_socket.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))#IP + Port "zusammenfuehren"
        #listen_socket.bind('', int(sys.argv[3])) => nur fuer loopback tests
    except:
        print ("Could not set up socket. (Listening)")
        sys.exit(1)

    listen_socket.listen(5) #listen starten, auf das SYN flooding warten
    listen_socket.accept() # Verbindung annehmen
    print("connected!")
    thread.interrupt_main()

#verbindet sich mit dem Server und Server traegt Addressen ein und sendet seine vorhandenen Addressen zurueck
def connect_to_server():
    try:
        srv_conn_socket = socket.socket()

        srv_conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Addresse wieder verwenden
        srv_conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)#Port wieder verwenden

        srv_conn_socket.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))#IP + Port "zusammenfuehren"
    except:
        print ("Could not set up socket. (SRV connection)")
        sys.exit(1)

    #srv_conn_socket.bind('', int(sys.argv[3]))
    while(srv_conn_socket.connect_ex((sys.argv[4], int(sys.argv[2])))):#SYN Packets an Server senden
        pass
    print("connected to server!")

    #daten von server bekommen
    srv_conn_socket.send("LR") #Daten eintragen und liste vom server bekommen
    #srv_conn_socket.send("R") #Daten vom server holen
    #srv_conn_socket.send("L") #Daten in liste eintragen

    utf_data=""
    try:
        data, addr = srv_conn_socket.recvfrom(1024)
        utf_data = data.decode('utf-8')
    except:
        print ("Could not receive messages.")
        sys.exit(1)
    print(utf_data)

    thread.interrupt_main()



def main():
    thread.start_new_thread(connect_to_server())
    thread.start_new_thread(connect(input("Ziel-IP des gewuenschten Kommunikationspartner:"), input("Ziel-Port des gewuenschten Kommunikationspartner:")))
    thread.start_new_thread(listen())

    while True:
        pass

if __name__ == '__main__':
    main()

