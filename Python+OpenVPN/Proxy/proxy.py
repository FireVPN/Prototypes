import socket, sys, threading

PEER=("10.0.0.2",6222)
LOCALVPN=""

EXT=("10.0.0.1", 6222)
INT=("127.0.0.1", 6221)

try:
    socket_int = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_int.bind(INT)
except:
    print ("Could not set up INT socket.")
    sys.exit(1)

try:
    socket_ext = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_ext.bind(EXT)
except:
    print ("Could not set up EXT socket.")
    sys.exit(1)

def int_to_ext():
    while True:
        data, addr = socket_int.recvfrom(32768)
        LOCALVPN=addr
        socket_ext.sendto(data, PEER)

def ext_to_int():
    while True:
        data, addr = socket_ext.recvfrom(32768)
        socket_int.sendto(data, LOCALVPN)



t_int_to_ext = threading.Thread(target=int_to_ext)
t_ext_to_int = threading.Thread(target=ext_to_int)
t_int_to_ext.start()
t_ext_to_int.start()