__author__ = 'Elias Eckenfellner'

import socket, sys, threading

SERVER=True
PEER=("10.0.0.2", 6222)
#Wenn Server
LOCALVPN=("127.0.0.1", 6220)

EXT=("10.0.0.1", 6222)
INT=("127.0.0.1", 6221)

#Immer 0
LOCALVPNPORT=0


socket_int_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket_int_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_int_rec.bind(INT)


socket_ext_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_ext_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_ext_rec.bind(EXT)

def int_to_ext():
    global LOCALVPNPORT
    global SERVER
    global LOCALVPN
    global socket_int_rec
    global socket_ext_send
    while True:
        data, addr = socket_int_rec.recvfrom(4096)
        if(not SERVER):
            LOCALVPNPORT=addr[1]
        socket_ext_send.sendto(data, PEER)
        print("int to ext")

def ext_to_int():
    global LOCALVPNPORT
    global SERVER
    global LOCALVPN
    global socket_int_send
    global socket_ext_rec
    while True:
        data, addr = socket_ext_rec.recvfrom(4096)
        if(not SERVER):
            socket_int_send.sendto(data, (INT[0], LOCALVPNPORT))
        if(SERVER):
            #socket_int_send.sendto(data, LOCALVPN)
            socket_int_rec.sendto(data, LOCALVPN)
        print("ext to int")


t_int_to_ext = threading.Thread(target=int_to_ext)
t_ext_to_int = threading.Thread(target=ext_to_int)
t_int_to_ext.start()
t_ext_to_int.start()