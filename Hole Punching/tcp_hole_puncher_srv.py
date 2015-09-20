__author__ = 'Alexander Mark, FireVPN'

import socket
import sys
import pickle

port = 12345
logins = set()
try:
    srv_socket = socket.socket()
    srv_socket.bind((socket.gethostname(), port))
except:
    print ("Could not set up socket.")
    sys.exit(1)
srv_socket.listen(5)

def receive():
    srv_socket.accept()
    data, addr = srv_socket.recvfrom(1024)
    host = addr[0]
    port = addr[1]
    utf_data = data.decode('utf-8')
    if utf_data is 'L':
        logins.add((host, port))
        print (logins)
    if utf_data is 'R':
        srv_socket.sendto(pickle.dumps(logins), (host, port))
        print ("sent reload.")
    if utf_data is 'LR':
        logins.add((host, port))
        print (logins)
        srv_socket.send(pickle.dumps(logins))
        print ("sent reload.")

def main():
    while True:
        receive()

if __name__ == '__main__':
    main()