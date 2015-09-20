__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter
# sys.argv[1] == IP Addresse (source)
# sys.argv[3] == Source Port
# sys.argv[2] == Destination Port (server)
# sys.argv[4] == Destination IP (server)


import sys
import socket
import _thread as thread

#sendet syn Packete aus während des hole punching prozesses
def connect(dest_ip,dest_port):
    connect_socket = socket.socket()

    connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    connect_socket.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))
    #connect_socket.bind('', int(sys.argv[3])) => nur für loopback tests
    while(connect_socket.connect_ex((dest_ip, dest_port))):
        pass
    print("connected!")
    thread.interrupt_main()

#listen für eingehende SYN Packets, während des hole punching prozesses. (Verbindungsannahme)
def listen():
    listen_socket = socket.socket()

    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    listen_socket.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))
    #listen_socket.bind('', int(sys.argv[3])) => nur für loopback tests
    listen_socket.listen(5)
    listen_socket.accept()
    print("connected!")
    thread.interrupt_main()

#verbindet sich mit dem Server und Server trägt Addressen ein und sendet seine vorhandenen Addressen zurück
def connect_to_server():
    srv_conn_socket = socket.socket()

    srv_conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_conn_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    srv_conn_socket.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[3])))
    print ("socket set up")
    #srv_conn_socket.bind('', int(sys.argv[3]))
    while(srv_conn_socket.connect_ex((sys.argv[4], int(sys.argv[2])))):
        pass
    print("connected to server!")
    srv_conn_socket.send("LR")

    utf_data=""
    try:
        data, addr = srv_conn_socket.recvfrom(1024)
        utf_data = data.decode('utf-8')
    except:
        print ("Could not receive messages.")
        sys.exit(1)
    print(utf_data)

    thread.interrupt_main()



def main():
    thread.start_new_thread(connect_to_server())
    thread.start_new_thread(connect(input("Ziel-IP des gewuenschten Kommunikationspartner:"), input("Ziel-Port des gewuenschten Kommunikationspartner:")))
    thread.start_new_thread(listen())

    while True:
        pass

if __name__ == '__main__':
    main()

