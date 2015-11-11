__author__ = 'Elias Eckenfellner'
HOST="127.0.0.1"
PORT=56
import argparse
import sys
import asyncio
import signal

SERVER=True
#Gegenüber von FireVPN
PEER=("10.0.0.2", 6222)
#Wenn Server
LOCALVPN=("127.0.0.1", 6220)

EXT=("10.0.0.1", 6222)
INT=("127.0.0.1", 6221)

#Immer 0
LOCALVPNPORT=0

class Serverrelay:

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print("datagram recieved")
        #Am Outside-Sockel senden
        #self.transport.sendto(data, addr)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)


class ClientRelay:

    def connection_made(self, transport):
        self.transport = transport
        print('sending "{}"'.format(self.message))
        self.transport.sendto(self.message.encode())
        print('waiting to receive')

    def datagram_received(self, data, addr):
        print('received "{}"'.format(data.decode()))
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('closing transport', exc)
        loop = asyncio.get_event_loop()
        loop.stop()


def start_server(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        Serverrelay, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport


def start_client(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        ClientRelay, remote_addr=addr))
    loop.run_until_complete(t)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if(SERVER):
        server = start_server(loop, INT)
    else:
        start_client(loop, (HOST, PORT))
    try:
        loop.run_forever()
    finally:
        if(SERVER):
            server.close()
        loop.close()