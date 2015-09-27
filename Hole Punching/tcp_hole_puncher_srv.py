__author__ = 'Alexander Mark, FireVPN'

import socket
import sys
import pickle

port = 9998
ip= "10.0.0.8"#(socket.gethostbyname(socket.gethostname()))
print (ip)
logins = set()

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden


    #srv_socket.bind(srv_socket.gethostname(), port) #auch fehlerhaft
srv_socket.bind((ip, port)) #IP + Port binden
srv_socket.listen(5) # auf Verbindungsanfragen lauschen

def receive():
    clientsocket,addr = srv_socket.accept() #verbindung annehmen
    data, addr = srv_socket.recvfrom(1024) #daten und adresse in variablen speichern
    host = addr[0]
    port = addr[1]
    utf_data = data.decode('utf-8') #charset fuer daten festlegen

    if utf_data is 'L': #wenn L empfangen wurde, addresse in set eintragen
        logins.add((host, port))
        print (logins)

    if utf_data is 'R': # wenn R empfangen wurde, addressen vom set an client senden
        try:
            clientsocket.send(pickle.dumps(logins))
        except:
            print ("Could not send. R")
        print ("sent reload. R")

    if utf_data is 'LR': # wenn LR empfangen wurde, addressen in set speichern, und danach zuruecksenden an Client
        logins.add((host, port))
        print (logins)
        try:
            clientsocket.send(pickle.dumps(logins))
        except:
            print ("Could not send. LR")
        print ("sent reload. LR")
    clientsocket.close()

def main():
    while True:
        receive()

if __name__ == '__main__':
    main()