__author__ = 'Alexander Mark'

import socket
import sys
import pickle

""""
Parameter nach dem File (zB.: python3 server.py 10.0.0.1 8888)
sys.argv[1] private IP des Hosts (zB.: 10.0.0.1)
sys.argv[2] Port des Hosts (zB.: 8888)
"""""

#empfangen und oeffentliche Addresse zuruecksenden
def receive():
    clientsocket =sock.accept()
    data=clientsocket[0].recv(1024)
    print ("received something")
    utf8_data=data.decode('utf-8')
    if utf8_data =="want Address" :
        clientsocket[0].send(pickle.dumps(clientsocket[1]))
        print("sent back data")

host_ip=sys.argv[1]
host_port =int(sys.argv [2])

#socket aufsetzten
sock = socket.socket()
sock.bind((host_ip,host_port))
sock.listen(5)
print ("set up port on ", host_ip, host_port)

#Addressen zurueck liefern
while(True): receive()

