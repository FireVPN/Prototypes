import socket, sys, threading

SERVER=True
PEER=("10.0.0.2", 6222)
LOCALVPN=("localhost", 6220)

EXT=("10.0.0.1", 6222)
INT=("localhost", 6221)

#Immer 0
localvpnport=0

try:
    socket_int_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_int_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_int_rec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_int_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_int_rec.bind(INT)
    socket_int_send.bind(INT)
    #Performance
    socket_int_rec.settimeout(1)
except:
    print ("Interner Socket konnte nicht initialisiert werden!")
    sys.exit(1)

try:
    socket_ext_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_ext_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_ext_rec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_ext_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_ext_rec.bind(EXT)
    socket_ext_send.bind(EXT)
    #Performance
    socket_ext_rec.settimeout(1)
except:
    print ("Externer Socket konnte nicht initialisiert werden!")
    sys.exit(1)


def int_to_ext():
    global localvpnport
    global SERVER
    global socket_int_rec
    global socket_ext_send
    while True:
        try:
            data, addr = socket_int_rec.recvfrom(4096)
            if(not SERVER):
                localvpnport=addr[1]
            socket_ext_send.sendto(data, PEER)
            print("int to ext")
        except:
            pass


def ext_to_int():
    global localvpnport
    global SERVER
    global LOCALVPN
    global socket_int_send
    global socket_ext_rec
    while True:
        try:
            data, addr = socket_ext_rec.recvfrom(4096)
            if(not SERVER):
                socket_int_send.sendto(data, ("localhost", localvpnport))
            if(SERVER):
                socket_int_send.sendto(data, LOCALVPN)
            print("ext to int")
        except:
            pass


t_int_to_ext = threading.Thread(target=int_to_ext)
t_ext_to_int = threading.Thread(target=ext_to_int)
t_int_to_ext.start()
t_ext_to_int.start()