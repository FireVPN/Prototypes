__author__ = 'Elias Eckenfellner'
import socket
IP="localhost"
PORT=6220

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print("Server lauscht auf", IP,":",PORT)
while True:
    data, addr = sock.recvfrom(2048)
    print("von", addr[0],":",addr[1], "empfangen")
    sock.sendto("Hello from Server".encode("UTF-8"), addr)
    print("an", addr[0],":",addr[1], "gesendet")