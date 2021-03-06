__author__ = 'Alexander Mark, FireVPN'

import socket
import sys
import pickle
#import _thread as thread
import threading as thread

port = 9999
ip= "10.0.0.10"#(socket.gethostbyname(socket.gethostname()))
print (ip)
logins = set()

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden


    #srv_socket.bind(srv_socket.gethostname(), port) #auch fehlerhaft
srv_socket.bind((ip, port)) #IP + Port binden
srv_socket.listen(5) # auf Verbindungsanfragen lauschen

def receive(clientsocket):
    addr=clientsocket[1]
    print (addr)
    while (True):
        data= clientsocket[0].recv(1024) #adresse in variable speichern
        #host = addr[0]
        #port = addr[1]
        utf_data = data.decode('utf-8') #charset fuer daten festlegen
        print (utf_data)

        if utf_data == 'L': #wenn L empfangen wurde, addresse in set eintragen
            logins.add(addr)
            print (logins)

        if utf_data == 'R': # wenn R empfangen wurde, addressen vom set an client senden
            try:
                clientsocket[0].send(pickle.dumps(logins))
            except:
                print ("Could not send. R")
            print ("sent reload. R")

        if utf_data ==  "LR": # wenn LR empfangen wurde, addressen in set speichern, und danach zuruecksenden an Client
            logins.add(addr)
            print (logins)
            try:
                clientsocket[0].send(pickle.dumps(logins))
            except:
                print ("Could not send. LR")
            print ("sent reload. LR")

        if utf_data is 'CLOSE': # wenn CLOSE empfangen wurde, Verbindung trennen
            clientsocket.close()



def main():
    while True:
        thread.Thread(target=receive(srv_socket.accept())).start() #mutlithreaded verbindungen annehmen und verarbeiten

if __name__ == '__main__':
    main()