__author__ = 'Alexander Mark, FireVPN'

import socket
import sys
import pickle

port = 12345
ip= "10.0.0.8"
logins = set()
try:
    srv_socket = socket.socket()
    srv_socket.bind(ip, port) #auch fehlerhaft
    #srv_socket.bind((socket.gethostbyname(srv_socket.gethostname()), port)) #IP + Port binden (socket_attribute hat die methoden laut traceback nicht)
except:
    print ("Could not set up socket.")
    sys.exit(1)
srv_socket.listen(5) # auf Verbindungsanfragen lauschen

def receive():
    srv_socket.accept() #verbindung annehmen
    data, addr = srv_socket.recvfrom(1024) #daten und adresse in variablen speichern
    host = addr[0]
    port = addr[1]
    utf_data = data.decode('utf-8') #charset fuer daten festlegen

    if utf_data is 'L': #wenn L empfangen wurde, addresse in set eintragen
        logins.add((host, port))
        print (logins)

    if utf_data is 'R': # wenn R empfangen wurde, addressen vom set an client senden
        try:
            srv_socket.send(pickle.dumps(logins))
        except:
            print ("Could not send. R")
        print ("sent reload. R")

    if utf_data is 'LR': # wenn LR empfangen wurde, addressen in set speichern, und danach zuruecksenden an Client
        logins.add((host, port))
        print (logins)
        try:
            srv_socket.send(pickle.dumps(logins))
        except:
            print ("Could not send. LR")
        print ("sent reload. LR")

def main():
    while True:
        receive()

if __name__ == '__main__':
    main()