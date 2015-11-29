__author__ = 'Alexander Mark, FireVPN'

import socket
import pickle

#Logik des Hole Puncher
class Client():

    #Konstruktor, Adresse des Hosts einlesen
    def __init__(self):
        print ("starting programm...")
        self.ip=input("IP des Hosts: ")
        self.port=4444
        print("IP + Port from Host saved")

    #Verbindung zu Server herstellen
    def connect_to_server(self):
        self.srv_ip=input("IP des Servers: ")
        self.srv_port=int(input("Port des Servers: "))
        print ("Got Server Adress")

        self.to_srv_sock = socket.socket()

        self.to_srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
        self.to_srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

        self.to_srv_sock.bind((self.ip, self.port)) #IP + Port "zusammenfuehren"
        print("Set up Socket (for Server Communication)")

        while(self.to_srv_sock.connect_ex((self.srv_ip, self.srv_port))): #SYN packets flooding
            pass
        print("connected to Server!")

    #Befehl zu Server senden (send list, refresh,...)
    def send_command_to_srv(self):
        print("#Mögliche Befehle: \n"
              "#R: Adressen von Server erhalten")
        self.command=input("Command for Server-Interaktion: ")
        self.to_srv_sock.send(self.command.encode('utf-8'))
        print (self.command, "send to Server")

        if self.command=='R':
            self.receive_from_srv()

    #von Server empfangen (informationen)
    def receive_from_srv(self):
        data =self.to_srv_sock.recv(1024)
        print ("received data from Server")
        self.available_adresses=pickle.loads(data)

        if len(self.available_adresses)==1:
            print("your Adress", self.available_adresses, "no others found, going back to command mode")
            self.send_command_to_srv()
        else:
            self.choose_addr()

    #addresse ausaehlen
    def choose_addr(self):
        print ("#available Adresses:")
        for (i in self.available_adresses):
            print ("#",i[0], ":", i[1])
        selected_adr=input("gewünschte Adresse (IP:Port): ")
        splited_adress=selected_adr.split(":")
        self.selected_ip=splited_adress[0]
        self.selected_port=int(splited_adress[1])


    #benoetigte sockets aufsetzen und hole punching prozess starten
    def prepare_punch(self):
        #do something

    def connect_to_Client(self):
        connect_socket = socket.socket()

        connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Addresse wieder verwenden
        connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Port wieder verwenden

        connect_socket.bind((self.ip, self.port)) #IP + Port "zusammenfuehren"
        #connect_socket.bind('', int(sys.argv[3])) => nur fuer loopback tests


        while(connect_socket.connect_ex((self.selected_ip, self.selected_port))): #SYN packets flooding
            pass
        print("connected!")
        #was nun?


def main():
    client=Client()
    client.connect_to_server()
    client.send_command_to_srv()


if __name__ == '__main__':
    main()

