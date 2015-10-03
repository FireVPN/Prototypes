import socket, sys, pickle

SERV_IP = "0.0.0.0"
SERV_PORT = 4567
logins = set()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERV_IP, SERV_PORT))
except:
    print ("Could not set up socket.")
    sys.exit(1)

def receive():
    data, addr = sock.recvfrom(1024)
    host = addr[0]
    port = addr[1]
    utf_data = data.decode('utf-8')
    print ("received")

    if utf_data is 'L':
        logins.add((host, port))
        print (logins)
    elif utf_data is 'R':
        sock.sendto(pickle.dumps(logins), (host, port))
        print ("sent reload.")

def main():
    while True:
        receive()

if __name__ == '__main__':
    main()
