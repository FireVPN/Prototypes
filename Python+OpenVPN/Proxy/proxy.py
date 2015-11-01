import sys, threading

EXT=("10.0.0.2", 6222)
LOCAL=("127.0.0.1", 6221)

def forward(listen):
    import socket
    try:
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.bind(listen)
    except:
        print ("Could not set up socket.")
        sys.exit(1)

