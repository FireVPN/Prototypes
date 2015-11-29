__author__ = 'Alexander Mark, FireVPN'

import socket

class Client():

    def __init__(self):
        print ("starting programm...")
        self.ip=input("IP des Hosts: ")
        self.port=4444
        print("IP + Port from Host saved")


    def connect_to_server(self):
        srv_ip=input("IP des Servers: ")
        srv_port=int(input("Port des Servers: "))
        print ("Got Server Adress")

        to_srv_sock = socket.socket()

        to_srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
        to_srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

        to_srv_sock.bind((self.ip, self.port)) #IP + Port "zusammenfuehren"
        print("Set up Socket (for Server Communication)")

        while(to_srv_sock.connect_ex((srv_ip, srv_port))): #SYN packets flooding
            pass
        print("connected to Server!")


def main():
    client=Client()
    client.connect_to_server()


if __name__ == '__main__':
    main()

