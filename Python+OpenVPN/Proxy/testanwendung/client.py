__author__ = 'Elias Eckenfellner'
import socket
IP="localhost"
#Vom OpenVPN-Client randomized
PORT=6532

PROXY=("localhost", 6221)

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print("Socket auf", IP,":",PORT, "gebunden")
sock.sendto("Hello from Client".encode("UTF-8"), PROXY)
print("An", PROXY, "gesendet")
data, addr = sock.recvfrom(2048)
print(data, "von", addr[0],":",addr[1], "empfangen")