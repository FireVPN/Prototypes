__author__ = 'Alexander Mark'
#uses python 3.4

import socket
import sys
import pickle

""""
Parameter nach dem File (zB.: python3 client.py 10.0.0.1 8888 1.2.3.4 60 5.6.7.8 70)
sys.argv[1] private IP des Hosts (zB.: 10.0.0.1)
sys.argv[2] Port des Hosts (zB.: 8888)
sys.argv[3] offizielle IP des 1. Servers (zB.: 1.2.3.4)
sys.argv[4] offizieller Port des 1. Servers (zB.: 60)
sys.argv[5] offizielle IP des 2. Servers (zB.: 5.6.7.8)
sys.argv[6] offizieller Port des 2. Servers (zB.: 70)
"""""

#zu Server verbinden und IP+Port zurueckliefer
def get_official_address(destination, sock):
    while(sock.connect_ex(destination)):
        pass
    sock.send("want Address".encode('utf-8'))
    data, server = sock.recvfrom(1024)
    return pickle.loads(data)


host_ip=sys.argv[1]
host_port =int(sys.argv [2])
srv0_ip=sys.argv[3]
srv0_port=int(sys.argv[4])
srv1_ip=sys.argv[5]
srv1_port=int(int(sys.argv[6]))

#socket aufsetzten
sock0 = socket.socket()
sock0.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
sock0.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden
sock0.bind((host_ip,host_port))
print ("set up port on (sock0)", host_ip, host_port)

sock1 = socket.socket()
sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden
sock1.bind((host_ip,host_port))
print ("set up port on (sock1)", host_ip, host_port)

#zu Server0 verbinden und IP+Port erhalten
addr_srv0 = get_official_address((srv0_ip,srv0_port), sock0)
print ("official Address from server0:", addr_srv0)

#zu Server1 verbinden und IP+Port erhalten
addr_srv1 = get_official_address((srv1_ip,srv1_port), sock1)
print ("official Address from server1:", addr_srv0)

#Addressen vergleichen
if (addr_srv0[0] == addr_srv1[0]):
    print("IP ist gleich")
else:
    print("IP hat sich veraendert")
if (addr_srv0[1] == addr_srv1[1]):
    print("Port ist gleich")
elif ((addr_srv0[1] - addr_srv1[1])==1):
    print ("Port ist um eines niedriger geworden")
elif ((addr_srv0[1] - addr_srv1[1])==-1):
    print ("Port ist um eines hoeher geworden")
else:
    print ("Port hat sich veraendert, kein einfaches Muster erkennbar")

